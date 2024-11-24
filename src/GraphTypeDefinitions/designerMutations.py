import typing
import strawberry

@strawberry.mutation(description="")
async def create_type(self, name: str) -> bool:
    return True

@strawberry.input(description="initial values for new field")
class ArgumentDefinition:
    name: str = strawberry.field(description="type name where field will be created")
    type_name: str = strawberry.field(description="type name where field will be created")

@strawberry.input(description="initial values for new field")
class FieldDefinition:
    type_name: str = strawberry.field(description="type name where field will be created")
    field_name: str = strawberry.field(description="name of new field will")
    result_type_name: str = strawberry.field(description="type name where field will be created")
    args: typing.List[ArgumentDefinition] = strawberry.field(description="list of arguments")

@strawberry.mutation(description="")
async def create_field(self, field: FieldDefinition) -> bool:
    return True
