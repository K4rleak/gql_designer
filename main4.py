import json

import strawberry.types
with open("./schemaofschema.json", "r", encoding="utf-8") as f:
    schemajson = json.load(f)

types = schemajson["__schema"]["types"]
for t in types:
    print(t)
    break

import typing
import os
import strawberry
import uuid
import src.DBFeeder as DBFeeder
import asyncio
from enum import Enum
from src.Dataloaders import getLoadersFromInfo, getUserFromInfo
from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from src.DBDefinitions import startEngine,ComposeConnectionString
from src.GraphTypeDefinitions import schema




#schema = strawberry.Schema(query=QueryGQL, mutation=MutationGql, types=(SchemaGQL, ))

query = """

  query IntrospectionQuery {
    __schema {
      queryType { name }
      mutationType { name }
      subscriptionType { name }
      types {
        ...FullType
      }
      directives {
        name
        description
        args {
          ...InputValue
        }
      }
    }
  }

  fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
      name
      description
      args {
        ...InputValue
      }
      type {
        ...TypeRef
      }
      isDeprecated
      deprecationReason
    }
    inputFields {
      ...InputValue
    }
    interfaces {
      ...TypeRef
    }
    enumValues(includeDeprecated: true) {
      name
      description
      isDeprecated
      deprecationReason
    }
    possibleTypes {
      ...TypeRef
    }
  }

  fragment InputValue on __InputValue {
    name
    description
    type { ...TypeRef }
    defaultValue
  }

  fragment TypeRef on __Type {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
        }
      }
    }
  }"""

# query = "{ schema { types { name } } }"
# root_value = {"value": "go"}
# introspectionresult = schema.execute_sync(query=query, root_value=root_value)
# print(introspectionresult.data)

connectionString = ComposeConnectionString()

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

    # makeDrop = os.getenv("DEMO", None) == "True"
    makeDrop=True
    # logging.info(f'starting engine for "{connectionString} makeDrop={makeDrop}"')

    initizalizedEngine = await startEngine(
        connectionstring=connectionString, makeDrop=makeDrop, makeUp=True
    )   
    
    async def initDBWithReport(initizalizedEngine):
        from src.DBFeeder import initDB    
        await initDB(initizalizedEngine)
        print("data initialized", flush=True)
    
    future = initDBWithReport(initizalizedEngine)
    asyncio.create_task(future)
    return initizalizedEngine



async def get_context(request: Request):
    asyncSessionMaker = await RunOnceAndReturnSessionMaker()
        
    from src.Dataloaders import createLoadersContext
    context = createLoadersContext(asyncSessionMaker)
    result = {**context}
    result["request"] = request
    return result


@asynccontextmanager
async def lifespan(app: FastAPI):
    initizalizedEngine = await RunOnceAndReturnSessionMaker()  
    yield


app = FastAPI(lifespan=lifespan)
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")