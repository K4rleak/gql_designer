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
from .template import db_model_template


class CodeGenerationInput:
    id: uuid.UUID = strawberry.field(default=None, description="primary key value")

async def create_db_model(info: strawberry.types.Info,type_: CodeGenerationInput):
    print("Vytvoreno")
    context = info.context
    type_loader = getLoadersFromContext(context=context).TypeModel
    field_loader = getLoadersFromContext(context=context).FieldModel
    type_loader = getLoadersFromContext(context=context).TypeModel
    field_loader = getLoadersFromContext(context=context).FieldModel

    type_row = await type_loader.load(type_.id)
    fields = await field_loader.filter_by(master_type_id=type_.id)
    fields = [*fields]
    type_row.fields = fields

    futures = (type_loader.load(field.oftype_id) for field in fields)
    values = await asyncio.gather(*futures)

    for field,value in zip(fields,values):
        field.of_type = value

    type_map = {
        "String": "String",
        "DateTime": "DateTime",
        "UUID": "String",
        "Boolean": "Boolean",
        "Int": "Integer"
    }

    # field_lines = []
    # for field, of_type in zip(fields, types_of_fields):
    #     # Default type
    #     column_type = type_map.get(of_type.name, "String")
    #     nullable = "True" if field.nullable else "False"
    #     fk = f", ForeignKey('{of_type.name.lower()}s.id')" if of_type.kind == "OBJECT" else ""

    #     line = f'    {field.name} = Column({column_type}{fk}, nullable={nullable}, comment="{field.description}")'
    #     field_lines.append(line)

    # Template variables
    class_name = f"{type_row.name}Model"
    tablename = type_row.name.lower() + "s"
    description = type_row.description or type_row.name

    model_str =  db_model_template.format(
        class_name=class_name,
        tablename=tablename,
        description=description,
    )
    print(field_lines)
    print(model_str)
