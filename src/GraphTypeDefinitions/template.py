fields_template = """class {{type_name}}GQLModel(BaseGQLModel):
   @classmethod
   def getLoader(cls, info: strawberry.types.Info):
       return getLoadersFromInfo(info).TypeModel
{{#fields}}

    {{name}}: typing.Optional[{{type}}] = strawberry.field(
        default=None,
        description="Facility name assigned by an administrator",
        permission_classes=[
            OnlyForAuthentized
        ]
        )
{{/fields}}"""