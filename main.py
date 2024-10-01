import json
import uuid

from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from pydantic import BaseModel

from src.GraphTypeDefinitions import schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

class Item(BaseModel):
    query: str
    variables: dict = {}
    operationName: str = None

def schemaUp(schema: dict):
    types = schema.get("types", None)
    if types is None:
        schema["types"] = types
    for type in types:
        if ("id" not in type):
            type["id"] = uuid.uuid4()


def schemaDown(schema: dict):
    pass

@asynccontextmanager
async def get_context(request: Request):
    with open("./schema.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    yield data
    with open(".schema.json", "w", encoding="utf-8") as f:
        json.dump(data, ensure_ascii=False, indent=4)

app = FastAPI(lifespan=lifespan)
# app.mount("/gql", graphql_app)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

@app.get("/gql")
async def graphiql(request: Request):
    return await graphql_app.render_graphql_ide(request)

@app.post("/gql")
async def apollo_gql(request: Request, item: Item):
    async with get_context(request) as context:
        schemaresult = await schema.execute(query=item.query, variable_values=item.variables, operation_name=item.operationName, context_value=context)
        result = {"data": schemaresult.data}
        if schemaresult.errors:
            result["errors"] = [f"{error}" for error in schemaresult.errors]
        return result

