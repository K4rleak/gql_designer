import uuid
import typing
import strawberry

FieldGQLModel = typing.Annotated["FieldGQLModel", strawberry.lazy(".FieldGQLModel")]
ArgGQLModel = typing.Annotated["ArgGQLModel", strawberry.lazy(".ArgGQLModel")]

@strawberry.type(description="GQL field type definition")
class TypeGQLModel:
    def __init__(self, datadict: dict):
        self.data = datadict

    @strawberry.field(description="primary key")    
    def id(self) -> typing.Optional[uuid.UUID]:
        return self.data.id("name", None)

    @strawberry.field(description="name")    
    def name(self) -> typing.Optional[str]:
        return self.data.get("name", None)

    @strawberry.field(description="description")    
    def description(self) -> typing.Optional[str]:
        return self.data.get("description", None)

    @strawberry.field(description="if it is deprecated")    
    def is_deprecated(self) -> typing.Optional[bool]:
        return self.data.get("is_deprecated", None)

    @strawberry.field(description="deprecated reason")    
    def deprecation_reason(self) -> typing.Optional[str]:
        return self.data.get("deprecation_reason", None)

    @strawberry.field(description="type")    
    def kind(self) -> typing.Optional[str]:
        return self.data.get("kind", None)  

    @strawberry.field(description="type")    
    def of_type(self) -> typing.Optional["TypeGQLModel"]:
        return self.data.get("of_type", None)
    
    pass