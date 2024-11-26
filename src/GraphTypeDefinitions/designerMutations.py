import typing
import uuid
import asyncio
import strawberry
import strawberry.types

from uoishelpers.resolvers import Insert, InsertError, Update, UpdateError, Delete, DeleteError
from ..Dataloaders import getLoadersFromContext

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
    name: str = strawberry.field(description="name of new field will")
    description: str = strawberry.field(description="name of new field will")
    result_type_name: str = strawberry.field(description="type name where field will be created")
    args: typing.List[ArgumentDefinition] = strawberry.field(description="list of arguments")
    oftype_id: strawberry.Private[uuid.UUID]
    master_type_id: strawberry.Private[uuid.UUID]

@strawberry.input(description="initial values for new field")
class TypeDefinition:
    name: str = strawberry.field(description="type name where field will be created")

@strawberry.mutation(description="")
async def create_type(self, info: strawberry.types.Info, type: TypeDefinition) -> typing.Optional[str]:
    context = info.context
    type_loader = getLoadersFromContext(context=context).TypeModel
    # field_loader = getLoadersFromContext(context=context).FieldModel
    try:
        dbrow = await type_loader.insert(type)
    except Exception as e:
        return f"{e}"
    return f"{dbrow is not None}"

@strawberry.mutation(description="")
async def create_field(self, info: strawberry.types.Info, field: FieldDefinition) -> typing.Optional[str]:
    context = info.context
    type_loader = getLoadersFromContext(context=context).TypeModel
    type_ids = [field.master_type_id, field.oftype_id]
    type_futures = [type_loader.load(id) for id in type_ids]
    type_rows = await asyncio.gather(*type_futures)
    
    field_loader = getLoadersFromContext(context=context).FieldModel
    try:
        dbrow = await field_loader.insert(type)
    except Exception as e:
        return f"{e}"
    return f"{dbrow is not None}"
