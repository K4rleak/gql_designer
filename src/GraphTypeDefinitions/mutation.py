import strawberry
import typing

@strawberry.type
class Mutation:
    @strawberry.field(description="""""")
    async def type_insert(
        self, info: strawberry.types.Info) -> "str":
        return "hello"