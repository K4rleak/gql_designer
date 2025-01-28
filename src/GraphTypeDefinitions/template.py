fields_template = """class {{type_name}}GQLModel(BaseGQLModel):
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
{{/fields}}"""