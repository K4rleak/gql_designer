import json

import strawberry.types
with open("./schemaofschema.json", "r", encoding="utf-8") as f:
    schemajson = json.load(f)

types = schemajson["__schema"]["types"]
for t in types:
    print(t)
    break

import typing
import strawberry
import uuid
from enum import Enum
from src.Dataloaders import getLoadersFromInfo, getUserFromInfo
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from src.DBDefinitions import startEngine
from src.GraphTypeDefinitions._GraphResolvers import encapsulateInsert, encapsulateDelete, encapsulateUpdate


@strawberry.type(name="My__InputValue")
class InputGQL:
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
    @strawberry.field(description="")
    def name(self, info: strawberry.types.Info) -> str:
        return ""
    
    @strawberry.field(description="")
    def description(self, info: strawberry.types.Info) -> str:
        return "description"
    
    @strawberry.field(description="")
    def args(self, info: strawberry.types.Info) -> typing.List["InputGQL"]:
        return []
    
    @strawberry.field(description="")
    def type(self, info: strawberry.types.Info) -> "TypeGQL":
        return None
    
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

    # @strawberry.field(description="")
    @alchemyfield(description="")
    def kind(self, info: strawberry.types.Info) -> "TypeKindGQL":
        return None
    
    @strawberry.field(description="")
    def name(self, info: strawberry.types.Info) -> str:
        return ""
    
    @strawberry.field(description="")
    def description(self, info: strawberry.types.Info) -> str:
        return "description"
    
    @strawberry.field(description="")
    def fields(self, info: strawberry.types.Info, include_deprecated: bool = True) -> typing.List["FieldGQL"]:
        return []
    
    @strawberry.field(description="")
    def interfaces(self, info: strawberry.types.Info) -> typing.List["TypeGQL"]:
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
        return None
    
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

    # publication_id: uuid.UUID = strawberry.field(description="The ID of the associated publication")
    # user_id: uuid.UUID = strawberry.field(description="The ID of the associated user")
    id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID - primary key", default_factory=lambda:uuid.uuid4())

    # order: Optional[int] = strawberry.field(description="The order of the Author in the publication", default=1)
    # share: Optional[float] = strawberry.field(description="The share of the Author in the publication", default=50)
    # valid: Optional[bool] = strawberry.field(description="Indicates whether the data is valid or not (optional)", default=True)
    # createdby: strawberry.Private[uuid.UUID] = None
    name: typing.Optional[str] = strawberry.field(description="The ID - primary key")
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

schema = strawberry.Schema(query=QueryGQL, mutation=MutationGql, types=(SchemaGQL, ))

query = """

  query IntrospectionQuery {
    __schema {
      queryType { name }
      mutationType { name }
      subscriptionType { name }
      types {
        ...FullType
      }
      directives {
        name
        description
        args {
          ...InputValue
        }
      }
    }
  }

  fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
      name
      description
      args {
        ...InputValue
      }
      type {
        ...TypeRef
      }
      isDeprecated
      deprecationReason
    }
    inputFields {
      ...InputValue
    }
    interfaces {
      ...TypeRef
    }
    enumValues(includeDeprecated: true) {
      name
      description
      isDeprecated
      deprecationReason
    }
    possibleTypes {
      ...TypeRef
    }
  }

  fragment InputValue on __InputValue {
    name
    description
    type { ...TypeRef }
    defaultValue
  }

  fragment TypeRef on __Type {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
        }
      }
    }
  }"""

query = "{ schema { types { name } } }"
root_value = {"value": "go"}
introspectionresult = schema.execute_sync(query=query, root_value=root_value)
print(introspectionresult.data)

async def get_context():
    return {#volat zde funkci je to v gql publ
    }

graphql_app = GraphQLRouter(schema, context_getter=get_context)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await startEngine()
    yield



app = FastAPI(lifespan=lifespan)

app.include_router(graphql_app, prefix="/graphql")