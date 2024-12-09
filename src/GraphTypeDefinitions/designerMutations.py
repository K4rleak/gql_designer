import typing
import uuid
import asyncio
import strawberry
import strawberry.types
import datetime
import chevron

from uoishelpers.resolvers import Insert, InsertError, Update, UpdateError, Delete, DeleteError
from ..Dataloaders import getLoadersFromContext

@strawberry.mutation(description="")
async def create_type(self, name: str) -> bool:
    return True

@strawberry.input(description="initial values for new field")
class ArgumentDefinition:
    name: str = strawberry.field(description="")
    description: typing.Optional[str] = strawberry.field(description="name of new field will", default=None)
    default_value: typing.Optional[str] = strawberry.field(description="name of new field will", default=None)
    type_name: str = strawberry.field(description="")
    field_name: str = strawberry.field(description="type name where field will be created")
    field_id: strawberry.Private[uuid.UUID] = None
    oftype_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="values for argument deletion")
class ArgumentDeleteModel:
    id: uuid.UUID
    # field_id: typing.Optional[uuid.UUID] = None

@strawberry.input(description="")
class ArgumentUpdateModel:
    #lastchange: datetime.datetime = strawberry.field(default=None, description="time stamp")
    id: uuid.UUID = strawberry.field(default=None, description="primary key value")
    field_id: typing.Optional[uuid.UUID] = strawberry.field(description="")
    oftype_id: typing.Optional[uuid.UUID] = strawberry.field(description="")
    default_value: typing.Optional[str] = strawberry.field(description="name of new field will", default=None)
    name: typing.Optional[str] = strawberry.field(description="")
    description: typing.Optional[str] = strawberry.field(description="name of new field will", default=None)



    # createdby: strawberry.Private[IDType] = None
    # rbacobject: strawberry.Private[IDType] = None


@strawberry.input(description="initial values for new field")
class FieldDefinition:
    type_name: str = strawberry.field(description="type name where field will be created")
    name: str = strawberry.field(description="name of new field will")
    description: str = strawberry.field(description="name of new field will")
    result_type_name: str = strawberry.field(description="type name where field will be created")
    args: typing.List[ArgumentDefinition] = strawberry.field(description="list of arguments")
    oftype_id: strawberry.Private[uuid.UUID] = None
    master_type_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="values for argument deletion")
class FieldDeleteModel:
    id: uuid.UUID
    # field_id: typing.Optional[uuid.UUID] = None

@strawberry.input(description="")
class FieldUpdateModel:
    #lastchange: datetime.datetime = strawberry.field(default=None, description="time stamp")
    id: uuid.UUID = strawberry.field(default=None, description="primary key value")
    oftype_id: typing.Optional[uuid.UUID] = strawberry.field(description="")
    master_type_id: typing.Optional[uuid.UUID] = strawberry.field(description="")
    name: typing.Optional[str] = strawberry.field(description="")
    description: typing.Optional[str] = strawberry.field(description="")

@strawberry.input(description="initial values for new field")
class TypeDefinition:
    name: str = strawberry.field(description="type name where field will be created")

@strawberry.input(description="values for argument deletion")
class TypeDeleteModel:
    id: uuid.UUID

@strawberry.input(description="initial values for new field")
class TypeUpdateModel:
    id: uuid.UUID = strawberry.field(default=None, description="primary key value")
    name: typing.Optional[str] = strawberry.field(description="")
    description: typing.Optional[str] = strawberry.field(description="")
    kind: typing.Optional[str] = strawberry.field(description="")
    isDeprecated: typing.Optional[bool] = strawberry.field(description="")
    deprecationReason: typing.Optional[str] = strawberry.field(description="")
    schema_id: typing.Optional[uuid.UUID] = strawberry.field(description="")

@strawberry.input(description="initial values for new field")
class CodeGenerationInput:
    id: uuid.UUID = strawberry.field(default=None, description="primary key value")
    #fields: typing.List[FieldDefinition] = strawberry.field(description="list of fields")

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
    dbrows = await type_loader.filter_by(name = field.type_name)
    dbrow = next(dbrows, None)
    field.master_type_id = dbrow.id

    dbrows = await type_loader.filter_by(name = field.result_type_name)
    dbrow = next(dbrows, None)
    field.oftype_id = dbrow.id


    # type_ids = [field.master_type_id, field.oftype_id]
    # type_futures = [type_loader.load(id) for id in type_ids]
    # type_rows = await asyncio.gather(*type_futures)

    field_loader = getLoadersFromContext(context=context).FieldModel
    try:
        dbrow = await field_loader.insert(field)
    except Exception as e:
        return f"{e}"
    return f"{dbrow is not None}"

@strawberry.mutation(description="")
async def create_arg(self, info: strawberry.types.Info, arg: ArgumentDefinition) -> typing.Optional[str]:
    context = info.context
    type_loader = getLoadersFromContext(context=context).TypeModel
    dbrows = await type_loader.filter_by(name = arg.type_name)
    dbrow = next(dbrows, None)
    arg.oftype_id = dbrow.id

    field_loader = getLoadersFromContext(context=context).FieldModel
    dbrows = await field_loader.filter_by(name = arg.field_name)
    dbrow = next(dbrows, None)
    #print(dbrow.id)
    arg.field_id = dbrow.id

    arg_loader = getLoadersFromContext(context=context).InputValueModel
    try:
        dbrow = await arg_loader.insert(arg)
    except Exception as e:
        return f"{e}"
    return f"{dbrow is not None}"

@strawberry.mutation(description="")
async def arg_remove(self, info: strawberry.types.Info, arg: ArgumentDeleteModel) -> typing.Optional[str]:
    context = info.context
    loader = getLoadersFromContext(context=context).InputValueModel

    try:
        await loader.delete(arg.id)
    except Exception as e:
        return f"{e}"
    return "Record deleted successfully."


async def field_remove_(info: strawberry.types.Info, field: FieldDeleteModel) -> typing.Optional[str]:
    context = info.context
    arg_loader = getLoadersFromContext(context=context).InputValueModel
    field_loader = getLoadersFromContext(context=context).FieldModel
    try:
        args = await arg_loader.filter_by(field_id = field.id)
        for arg in args:
            print(arg.id)
            await arg_loader.delete(arg.id)

        await field_loader.delete(field.id)
    except Exception as e:
        return f"{e}"
    return "Record deleted successfully."

field_remove=strawberry.mutation(description="")(field_remove_)

@strawberry.mutation(description="")
async def type_remove(self, info: strawberry.types.Info, type: TypeDeleteModel) -> typing.Optional[str]:
    context = info.context
    type_loader = getLoadersFromContext(context=context).TypeModel
    field_loader = getLoadersFromContext(context=context).FieldModel
    try:
        fields = await field_loader.filter_by(master_type_id = type.id)
        for field in fields:
            await field_remove_(info=info,field=FieldDeleteModel(id=field.id))
        await type_loader.delete(type.id)
    except Exception as e:
        return f"{e}"
    return "Record deleted successfully."

@strawberry.mutation(description="")
async def arg_update(self, info: strawberry.types.Info, arg: ArgumentUpdateModel) -> typing.Optional[str]:
    context = info.context
    arg_loader = getLoadersFromContext(context=context).InputValueModel
    try:
        await arg_loader.update(arg)
    except Exception as e:
        return f"{e}"
    return "Record updated successfully."

@strawberry.mutation(description="")
async def field_update(self, info: strawberry.types.Info, field: FieldUpdateModel) -> typing.Optional[str]:
    context = info.context
    loader = getLoadersFromContext(context=context).FieldModel
    try:
        await loader.update(field)
    except Exception as e:
        return f"{e}"
    return "Record updated successfully."

@strawberry.mutation(description="")
async def type_update(self, info: strawberry.types.Info, type: TypeUpdateModel) -> typing.Optional[str]:
    context = info.context
    loader = getLoadersFromContext(context=context).TypeModel
    try:
        await loader.update(type)
    except Exception as e:
        return f"{e}"
    return "Record updated successfully."

@strawberry.mutation(description="")
async def generate_python_code(self, info: strawberry.types.Info, type: CodeGenerationInput) -> typing.Optional[str]:
    from .template import fields_template
    context = info.context
    type_loader = getLoadersFromContext(context=context).TypeModel
    field_loader = getLoadersFromContext(context=context).FieldModel

    type_row = await type_loader.load(type.id)
    fields = await field_loader.filter_by(master_type_id = type.id)
    fields = [*fields]
    type_row.fields = fields
    futures = (type_loader.load(field.oftype_id) for field in fields)
    values = await asyncio.gather(*futures)

    for field,value in zip(fields,values):
        field.of_type = value

    
    #elementary_types = {"int", "str", "bool", "float", "datetime.datetime", "IDType", "uuid.UUID"}

    field_data = [
        {
            "name": field.name,
            "type": field.of_type.name,
            #pokud null tak jedu dal na dalsi oftype.oftpye
            #"needs_resolver": "GQLModel" in field.of_type.name
            "is_vector": field.of_type.name == "null",
            "resolver": f'ScalarResolver["{field.of_type.name}GQLModel"](fkey_field_name="{field.name}_id")'
        }
        for field in fields
    ]

    for field in fields:
        print(field.of_type.name)
    data = {
    "fields": field_data,
    "type_name": type_row.name
}

    # fields_template = """{{#fields}}
    # {{name}}: typing.Optional[{{type}}] = strawberry.field(
    #     default=None,
    #     description="Facility name assigned by an administrator",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ]
    #     )
    # {{/fields}}"""

#     for attr, value in vars(type).items():
        # code_lines.extend([f"   {attr}: typing.Optional[str] = strawberry.field(",
        #            "       default=None,",
        #            '       description="""Facility name assigned by an administrator""",',
        #            "       permission_classes=[",
        #            "           OnlyForAuthenticated",
        #            "       ]",
        #            "   )"
# ])
    #generated_code = "\n".join(code_lines)
    #print(generated_code)
    result = chevron.render(fields_template, data)
    #print(result)
    return result



