import typing
import uuid
import asyncio
import strawberry
import strawberry.types
import datetime
import chevron

from uoishelpers.resolvers import Insert, InsertError, Update, UpdateError, Delete, DeleteError
from ..Dataloaders import getLoadersFromContext
from .TypeNameResolver import TypeNameResolver
from .db_model_creator import create_db_model

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
async def generate_python_code(self, info: strawberry.types.Info, type_: CodeGenerationInput) -> typing.Optional[str]:
    from .template import model_template
    context = info.context
    type_loader = getLoadersFromContext(context=context).TypeModel
    field_loader = getLoadersFromContext(context=context).FieldModel

    type_row = await type_loader.load(type_.id)
    fields = await field_loader.filter_by(master_type_id = type_.id)
    fields = [*fields]
    type_row.fields = fields
    futures = (type_loader.load(field.oftype_id) for field in fields)
    values = await asyncio.gather(*futures)
    #print(type_row.__tablename__)

    for field,value in zip(fields,values):
        field.of_type = value

    db_model_str = await create_db_model(info,type_.id)




    lazy_models=[]

    async def recursive(oftype_id,field):
        type_ = await type_loader.load(oftype_id)

        type_map={
            "String":"str",
            "DateTime": "datetime.datetime",
            "UUID":"IDType",
            "Boolean":"bool",
            "Int":"int"
        }

        innerName = ""
        if type_.oftype_id:
            # Recursive call and unpacking the result
            innerName, _ = await recursive(type_.oftype_id,field)
        if type_.kind == "SCALAR":
            #type_name=type(TypeNameResolver(type_)).__name__

            type_name=type_map.get(type_.name, None)
            

            return f"""typing.Optional[{type_name}]""", ""

        if type_.kind == "OBJECT":
            lazy_models.append({"name": f"{type_.name}"})
            return f"""typing.Optional["{type_.name}"]""", f"""resolver=ScalarResolver["{type_.name}"](fkey_field_name="{field.name}_id")"""

        if type_.kind == "LIST":
            # Use the string innerName instead of the entire tuple
            ReturnTypeOfList = await type_loader.load(type_.oftype_id)
            if ReturnTypeOfList.name in type_map:
                ReturnType = (f"{ReturnTypeOfList.name}") 
            else: 
                ReturnType = (f"{ReturnTypeOfList.name}GQLModel")
            innerName = innerName.replace("typing.Optional[\"", "").replace("\"]", "").replace("typing.Optional[", "").replace("]", "")
            if innerName in type_map.values():
                innerName 
            else: 
                innerName+="GQLModel"
            return f"""typing.List["{innerName}"]""", f"""resolver=VectorResolver["{ReturnType}"](fkey_field_name="{field.name}_id", whereType=None)"""
        #master type mysto toho type.name

        if type_.kind == "NON_NULL":
            return f"{innerName}", "skibidi"
        raise Exception("Missing type")

    

    #elementary_types = {"int", "str", "bool", "float", "datetime.datetime", "IDType", "uuid.UUID"}
    #print(field.of_type.kind)
    # async def TypeNameFromField(field):
    #     FieldReturnType = await recursive(field.of_type.id,field)
    #     TypeNameResolved=TypeNameResolver(FieldReturnType[0])
    #     if isinstance(TypeNameResolved, str):
    #         return (TypeNameResolved, FieldReturnType[1])
    #     else:
    #         return (type(TypeNameResolved).__name__, FieldReturnType[1])

    
    field_data = [
        {
            "name": field.name,
            "type": field.of_type.name,
            "description": field.description,
            # Unpack the return values from recursive
            "return_type": (return_type := await recursive(field.of_type.id,field))[0],
            "resolver": return_type[1],
            "has_resolver": bool(return_type[1])
        }
        for field in fields
    ]

    # for field in fields:
    #     result = await recursive(field.of_type.id)  # Await the result
    #     print(result)

   
    TypeNameResolved=TypeNameResolver(type_row)

    if isinstance(TypeNameResolved,str):
        pass
    else:
        TypeNameResolved= type(TypeNameResolved).__name__
    
    type_data = {
    "fields": field_data,
    "type_name": TypeNameResolved,
    "type_description" : type_row.description,
    "table_name": type_row.__tablename__,
    "lazy_models": lazy_models
}
    #     type_data = {
    #         "fields": field_data,
    #         "type_name": TypeNameResolved,
    #         "table_name": type_row.__tablename__
    #     }
    # else:
    #     type_data = {
    #         "fields": field_data,
    #         "type_name": type(TypeNameResolved).__name__,
    #         "table_name": type_row.__tablename__
    #     }


    result = chevron.render(model_template, type_data)
    #print(result)
    return result



