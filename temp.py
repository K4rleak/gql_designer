class FacilityGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
       return getLoadersFromInfo(info).types

    id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    nameEn: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    lastchange: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    created: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    label: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    address: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    valid: typing.Optional[bool] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    capacity: typing.Optional[int] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    geometry: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )

    geolocation: typing.Optional[str] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]        )