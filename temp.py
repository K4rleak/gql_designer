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
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
firsttype = typing.Annotated["firsttype", strawberry.lazy(".firsttype")]

@strawberry.federation.type(
    keys=["id"], description="Entity representing a Facility"
)
class FacilityGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
       return getLoadersFromInfo(info).types

    id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="Entity primary key",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="Name ",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    nameEn: typing.Optional[str] = strawberry.field(
        default=None,
        description="English name",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    lastchange: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="Time of last update",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    created: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="Time of entity introduction",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    label: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility full name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    address: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility address",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    valid: typing.Optional[bool] = strawberry.field(
        default=None,
        description="is the facility still valid",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    capacity: typing.Optional[int] = strawberry.field(
        default=None,
        description="Facility's capacity",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    geometry: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility geometry (SVG)",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    geolocation: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility geo address (WGS84+zoom)",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    changedby: typing.Optional["UserGQLModel"] = strawberry.field(
        default=None,
        description="Who made last change",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["UserGQLModelGQLModel"](fkey_field_name="changedby_id")
        )

    reservations: typing.List["firsttype"] = strawberry.field(
        default=None,
        description="Intermediate entity linking the event and facility",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["firsttypeGQLModel"](fkey_field_name="reservations_id", whereType=None)
        )

    externalIds: typing.List[IDType] = strawberry.field(
        default=None,
        description="All related external ids",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["UUIDGQLModel"](fkey_field_name="externalIds_id", whereType=None)
        )