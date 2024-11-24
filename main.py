import asyncio
import os
import pydantic
import dataclasses
import logging

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from contextlib import asynccontextmanager

# from src.GraphTypeDefinitions import schema
from src.DBDefinitions import ComposeConnectionString, startEngine
from src.GraphTypeDefinitions import createSchema
from src.SchemaLoad import loadSchema
from src.Dataloaders import createLoadersContext

def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result

@singleCall
async def RunOnceAndReturnSessionMaker():
    """Provadi inicializaci asynchronniho db engine, inicializaci databaze a vraci asynchronni SessionMaker.
    Protoze je dekorovana, volani teto funkce se provede jen jednou a vystup se zapamatuje a vraci se pri dalsich volanich.
    """
    connectionString = ComposeConnectionString()
    makeDrop = os.getenv("DEMO", None) == "True"
    logging.info(f'starting engine for "{connectionString} makeDrop={makeDrop}"')

    result = await startEngine(
        connectionstring=connectionString, makeDrop=makeDrop, makeUp=True
    )   

    ###########################################################################################################################
    #
    # zde definujte do funkce asyncio.gather
    # vlozte asynchronni funkce, ktere maji data uvest do prvotniho konzistentniho stavu
    #
    #
    ###########################################################################################################################
    from src.DBFeeder import initDB
    future = initDB(result)
    asyncio.create_task(future)
    return result

@asynccontextmanager
async def lifespan(app: FastAPI):
    # loadSchema()
    await RunOnceAndReturnSessionMaker()
    logging.info("life od FastAPI begins")
    yield
    logging.info("life od FastAPI ends")

@asynccontextmanager
async def get_context(request: Request):
    # with open("./schema.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    
    yield 
    # with open(".schema.json", "w", encoding="utf-8") as f:
    #     json.dump(data, ensure_ascii=False, indent=4)

app = FastAPI(lifespan=lifespan)
# app.mount("/gql", graphql_app)

class Item(pydantic.BaseModel):
    query: str
    variables: dict = None
    operationName: str = None

@app.post("/gql", response_class=JSONResponse)
async def apigql_post(data: Item, request: Request):
    gqlQuery = {}
    if (data.operationName) is not None:
        gqlQuery["operationName"] = data.operationName

    gqlQuery["query"] = data.query
    if (data.variables) is not None:
        gqlQuery["variables"] = data.variables

    seesionMaker = await RunOnceAndReturnSessionMaker()
    context = createLoadersContext(seesionMaker)
    schema = await createSchema(context=context)
    result = await schema.execute(
        query=data.query, 
        variable_values=data.variables,
        operation_name=data.operationName
        )
    
    return dataclasses.asdict(result)
    
@app.get("/gql", response_class=FileResponse)
async def graphiql():
    realpath = os.path.realpath("./graphiql.html")
    return realpath

@app.get("/voyager", response_class=FileResponse)
async def graphiql():
    realpath = os.path.realpath("./voyager.html")
    return realpath


logger = logging.getLogger()
logger.setLevel(logging.INFO)