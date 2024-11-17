import json

from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from src.GraphTypeDefinitions import schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

@asynccontextmanager
async def get_context(request: Request):
    with open("./schema.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    yield data
    with open(".schema.json", "w", encoding="utf-8") as f:
        json.dump(data, ensure_ascii=False, indent=4)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)


app = FastAPI(lifespan=lifespan)
# app.mount("/gql", graphql_app)

app.include_router(graphql_app, prefix="/gql")
