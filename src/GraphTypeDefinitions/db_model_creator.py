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

async def create_db_model(info: strawberry.types.Info,type_id):
    print(f"Vytvoreno s id:{type_id}", flush=True)
    context = info.context
    return await create_db_model_context(context,type_id)

async def create_db_model_context(context,type_id):
    print(f"Vytvoreno s id:{type_id}", flush=True)
    type_loader = getLoadersFromContext(context=context).TypeModel
    field_loader = getLoadersFromContext(context=context).FieldModel

    type_row = await type_loader.load(type_id)
    assert type_row is not None, "Nenalezen"
    fields = await field_loader.filter_by(master_type_id=type_id)
    fields = list(fields)

    type_row.fields = fields

    futures = (type_loader.load(field.oftype_id) for field in fields)
    types_of_fields = await asyncio.gather(*futures)

    type_map = {
        "String": "String",
        "DateTime": "DateTime",
        "UUID": "String",
        "Boolean": "Boolean",
        "Int": "Integer"
    }

    field_lines = []
    for field, of_type in zip(fields, types_of_fields):
        # Default type
        column_type = type_map.get(of_type.name, "String")
        #nullable = "True" if field.nullable else "False"
        fk = f", ForeignKey('{of_type.name.lower()}s.id')" if of_type.kind == "OBJECT" else ""
        #if nullable:
        #line = f'    {field.name} = Column({column_type}{fk}, nullable=, comment="{field.description}")'
        line = f'    {field.name} = Column({column_type}{fk}, nullable=True, comment="{field.description}")'
        field_lines.append(line)

    # Template variables
    class_name = f"{type_row.name}"
    tablename = type_row.name.lower() + "s"
    description = type_row.description or type_row.name

    model_str= db_model_template.format(
        class_name=class_name,
        tablename=tablename,
        description=description,
        fields="\n".join(field_lines)
    )
    print(model_str)
