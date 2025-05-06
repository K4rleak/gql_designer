model_template = """
import asyncio
import dataclasses
import typing
import strawberry

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)

from .BaseGQLModel import BaseGQLModel, IDType
{{#lazy_models}}
{{name}} = typing.Annotated["{{name}}", strawberry.lazy(".{{name}}")]
{{/lazy_models}}

@strawberry.federation.type(
    keys=["id"], description="{{type_description}}"
)
class {{type_name}}GQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
       return getLoadersFromInfo(info).{{table_name}}
{{#fields}}

    {{name}}: {{{return_type}}} = strawberry.field(
        default=None,
        description="{{{description}}}",
        permission_classes=[
            OnlyForAuthentized
        ]{{#has_resolver}},
        {{{resolver}}}
        {{/has_resolver}}
        )
{{/fields}}


"""

db_model_template = '''import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel

class {class_name}(BaseModel):
    """{description}"""
    
    __tablename__ = "{tablename}"

{fields}
'''