# gql/type_gql.py

import strawberry
import typing
import dataclasses
from typing import Optional
from uoishelpers.resolvers import (
    getLoadersFromInfo,
    PageResolver, 
    createInputs,)

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
)   

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a Facility"""
)
class TemplateGQLModel():
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).TemplateModel
 
    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Template name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
        )

@createInputs
@dataclasses.dataclass
class TemplateInputFilter:
    name: str
    name_en: str
    valid: bool
    label: str
    capacity: int

template_page = strawberry.field(
        description="""Finds paged templates""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[TemplateGQLModel](whereType=TemplateInputFilter)
        )    