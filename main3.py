import json

import strawberry.types
with open("./schemaofschema.json", "r", encoding="utf-8") as f:
    schemajson = json.load(f)

types = schemajson["__schema"]["types"]
for t in types:
    print(t)
    break

import typing
import strawberry
import uuid
from enum import Enum
from src.Dataloaders import getLoadersFromInfo, getUserFromInfo
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from src.DBDefinitions import startEngine
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

query = "{ schema { types { name } } }"
root_value = {"value": "go"}
introspectionresult = schema.execute_sync(query=query, root_value=root_value)
print(introspectionresult.data)

async def get_context():
    return {#volat zde funkci je to v gql publ
    }

graphql_app = GraphQLRouter(schema, context_getter=get_context)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await startEngine(makeDrop=True)
    yield



app = FastAPI(lifespan=lifespan)

app.include_router(graphql_app, prefix="/graphql")