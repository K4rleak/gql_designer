import typing
import asyncio
from typing import List, Union, Optional
import strawberry
import strawberry.types
import uuid
import datetime
from enum import Enum
from src.Dataloaders import getLoadersFromInfo, getUserFromInfo
from src.GraphTypeDefinitions._GraphResolvers import encapsulateInsert, encapsulateDelete, encapsulateUpdate
#import z uois helpers podivat se do facillities

# from contextlib import asynccontextmanager


# @asynccontextmanager
# async def withInfo(info):
#     asyncSessionMaker = info.context["asyncSessionMaker"]
#     async with asyncSessionMaker() as session:
#         try:
#             yield session
#         finally:
#             pass


# def getLoader(info):
#     return info.context["all"]


import datetime
    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

from .query import Query
from .mutation import Mutation

# from .userGQLModel import UserGQLModel # jen jako demo
# from .groupGQLModel import GroupGQLModel
# from .groupTypeGQLModel import GroupTypeGQLModel
# from .membershipGQLModel import MembershipGQLModel
# from .roleGQLModel import RoleGQLModel
# from .roleCategoryGQLModel import RoleCategoryGQLModel
# from .roleTypeGQLModel import RoleTypeGQLModel




@strawberry.type(name="My__InputValue")
class InputGQL:
    # @classmethod
    # def getloader(cls,info: strawberry.types.Info):
    #     loader = getLoadersFromInfo(info=info).
    @strawberry.field(description="")
    def name(self, info: strawberry.types.Info) -> str:
        return ""
    
    @strawberry.field(description="")
    def description(self) -> str:
        return "description"

    @strawberry.field(description="")
    def type(self) -> "TypeGQL":
        return None

    def default_value(self) -> str:
        return ""

@strawberry.type(name="My__EnumValue")
class EnumGQL:
    @strawberry.field(description="")
    def name(self, info: strawberry.types.Info) -> str:
        return ""
    
    @strawberry.field(description="")
    def description(self) -> str:
        return "description"

    @strawberry.field(description="")
    def is_deprecated(self) -> bool:
        return False
    
    @strawberry.field(description="")
    def deprecation_reason(self) -> str:
        return ""


@strawberry.type(name="My__Field")
class FieldGQL:
    @classmethod
    def getLoader(cls, info): 
        return getLoadersFromInfo(info).GQLFieldModel
    @classmethod
    async def resolve_reference(cls,info: strawberry.types.Info,id:uuid.UUID):
        #pozor jestli je id typu uuid nebo str
        loader=cls.getLoader(info)
        instance=await loader.load(id)
        instance.__strawberry_definition__=cls.__strawberry_definition__
        return instance
    
    @strawberry.field(description="")
    def name(self, info: strawberry.types.Info) -> str:
        return ""
    
    @strawberry.field(description="blabla")
    def description(self, info: strawberry.types.Info) -> str:
        return "description"
    
    @strawberry.field(description="blabla")
    async def master_type(self, info: strawberry.types.Info) -> typing.Optional["TypeGQL"]:
        result = await TypeGQL.resolve_reference(info=info,id=self.master_type_id)
        return result

    @strawberry.field(description="")
    def args(self, info: strawberry.types.Info) -> typing.List["InputGQL"]:
        return []
    
    @strawberry.field(description="type of this field")
    async def type(self, info: strawberry.types.Info) -> typing.Optional["TypeGQL"]:
        result = await TypeGQL.resolve_reference(info=info,id=self.typeof_id)
        return result
    
    @strawberry.field(description="")
    def is_deprecated(self, info: strawberry.types.Info) -> bool:
        return False
    
    @strawberry.field(description="")
    def deprecation_reason(self, info: strawberry.types.Info) -> str:
        return ""

@strawberry.enum(name="My__TypeKind")
class TypeKindGQL(Enum):
    SCALAR = "SCALAR"
    OBJECT = "OBJECT"
    INTERFACE = "INTERFACE"
    UNION = "UNION"
    ENUM = "ENUM"
    INPUT_OBJECT = "INPUT_OBJECT"
    LIST = "LIST"
    NON_NULL = "NON_NULL"

@strawberry.enum(name="My__DirectiveLocation")
class DirectiveLocationGQL(Enum):
    QUERY = "QUERY"
    MUTATION = "MUTATION"
    SUBSCRIPTION = "SUBSCRIPTION"
    FIELD = "FIELD"
    FRAGMENT_DEFINITION = "FRAGMENT_DEFINITION"
    FRAGMENT_SPREAD = "FRAGMENT_SPREAD"
    INLINE_FRAGMENT = "INLINE_FRAGMENT"
    SCHEMA = "SCHEMA"
    SCALAR = "SCALAR"
    OBJECT = "OBJECT"
    FIELD_DEFINITION = "FIELD_DEFINITION"
    ARGUMENT_DEFINITION = "ARGUMENT_DEFINITION"
    INTERFACE = "INTERFACE"
    UNION = "UNION"
    ENUM = "ENUM"
    ENUM_VALUE = "ENUM_VALUE"
    INPUT_OBJECT = "INPUT_OBJECT"
    INPUT_FIELD_DEFINITION = "INPUT_FIELD_DEFINITION"

@strawberry.type(name="My__Directive")
class DirectiveGQL:
    @strawberry.field(description="")
    def name(self, info: strawberry.types.Info) -> str:
        return ""
    
    @strawberry.field(description="")
    def description(self, info: strawberry.types.Info) -> str:
        return "description"

    @strawberry.field(description="")
    def locations(self, info: strawberry.types.Info) -> typing.List["DirectiveLocationGQL"]:
        return []

    @strawberry.field(description="")
    def args(self, info: strawberry.types.Info) -> typing.List["InputGQL"]:
        return []

import inspect
def alchemyfield(fieldFunc=None, /, **kwargs):   
    def result(fieldFunc):
        annotations = inspect.get_annotations(fieldFunc)
        print(f"annotations: {annotations}")
        print(f"fieldFunc: {fieldFunc.__name__}")
        return strawberry.field(fieldFunc, **kwargs)
    
    return result if fieldFunc is None else result(fieldFunc)

@strawberry.type(name="My__Type")
class TypeGQL:
    @classmethod
    def getLoader(cls, info): 
        return getLoadersFromInfo(info).GQLTypeModel
    data: strawberry.Private[object]

    @classmethod
    async def resolve_reference(cls,info: strawberry.types.Info,id:uuid.UUID):
        #pozor jestli je id typu uuid nebo str
        loader=cls.getLoader(info)
        instance=await loader.load(id)
        instance.__strawberry_definition__=cls.__strawberry_definition__
        return instance


    # @strawberry.field(description="")
    @alchemyfield(description="")
    def kind(self, info: strawberry.types.Info) -> "TypeKindGQL":
        return self.kind
    
    @strawberry.field(description="")
    def name(self, info: strawberry.types.Info) -> str:
        return self.name
    
    @strawberry.field(description="")
    def description(self, info: strawberry.types.Info) -> str:
        return self.description
    
    @strawberry.field(description="")
    def is_deprecated(self, info: strawberry.types.Info) -> bool:
        return self.isDeprecated
    
    @strawberry.field(description="")
    def deprecation_reason(self, info: strawberry.types.Info) -> str:
        return self.deprecationReason

    @strawberry.field(description="")
    async def fields(self, info: strawberry.types.Info, include_deprecated: bool = True) -> typing.List["FieldGQL"]:
        id = self.id
        loader = FieldGQL.getLoader(info=info)
        rows = await loader.filter_by(master_type_id=id)
        futures=(FieldGQL.resolve_reference(info=info,id=row.id)for row in rows)
        results=await asyncio.gather(*futures)
        return results
    
    @strawberry.field(description="")
    def interfaces(self, info: strawberry.types.Info) -> typing.List["TypeGQL"]:
        raise NotImplementedError("This method is not implemented yet.")
        return []
    
    @strawberry.field(description="")
    def possible_types(self, info: strawberry.types.Info) -> typing.List["TypeGQL"]:
        return []
    
    @strawberry.field(description="")
    def enum_values(self, info: strawberry.types.Info, include_deprecated: bool = True) -> typing.List["EnumGQL"]:
        return []
    
    @strawberry.field(description="")
    def input_fields(self, info: strawberry.types.Info) -> typing.List["InputGQL"]:
        return []
    
    @strawberry.field(description="")
    def of_type(self, info: strawberry.types.Info) -> "InputGQL":
        return self.typeof_id
    
    pass

@strawberry.type(name="My__Schema")
class SchemaGQL:
    @strawberry.field(description="")
    def types(self, info: strawberry.types.Info) -> typing.Optional[typing.List["TypeGQL"]]:
        print(info.root_value)
        return []
    
    @strawberry.field(description="")
    def query_type(self, info: strawberry.types.Info) -> "TypeGQL":
        return None
    
    @strawberry.field(description="")
    def mutation_type(self, info: strawberry.types.Info) -> typing.Optional["TypeGQL"]:
        return None
    
    @strawberry.field(description="")
    def subscription_type(self, info: strawberry.types.Info) -> typing.Optional["TypeGQL"]:
        return None
    
    @strawberry.field(description="")
    def directives(self, info: strawberry.types.Info) -> typing.Optional[typing.List["DirectiveGQL"]]:
        return []
    
@strawberry.type()
class QueryGQL:
    @strawberry.field(description="")
    def schema(self, info: strawberry.types.Info) -> "SchemaGQL":
        result = SchemaGQL()
        return result

@strawberry.input(description="")
class TypeInsertGQLModel:

    id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID - primary key", default_factory=lambda:uuid.uuid4())
    name: typing.Optional[str] = strawberry.field(description="The name")
    description: typing.Optional[str] = strawberry.field(description="The ID - primary key")
    kind: typing.Optional[str] = strawberry.field(description="The ID - primary key")
    isDeprecated: typing.Optional[bool] = strawberry.field(description="The ID - primary key")
    deprecationReason: typing.Optional[str] = strawberry.field(description="The ID - primary key")

    typeof_id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID - primary key")

@strawberry.type(description="Result of mutation")
class TypeResultGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID - primary key", default_factory=lambda:uuid.uuid4())
    msg: str = strawberry.field(description="Result of the operation (ok/fail)", default=None)
    
    @strawberry.field(description="Returns the author")
    async def type(self, info: strawberry.types.Info) -> typing.Optional["TypeGQL"]:
        result = await TypeGQL.resolve_reference(info, self.id)
        return result

@strawberry.type()    
class MutationGql:
    @strawberry.field(description="""""")
    async def type_insert(
        self, info: strawberry.types.Info, type: TypeInsertGQLModel) -> "TypeResultGQLModel":
        return await encapsulateInsert(info, TypeGQL.getLoader(info), type, TypeResultGQLModel(id=type.id, msg="ok"))










schema = strawberry.federation.Schema(query=Query, mutation=Mutation, types=(TypeGQL,))
# schema = strawberry.federation.Schema(query=Query)
