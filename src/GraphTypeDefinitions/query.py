import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .TypeGQLModel import type_page
    pass