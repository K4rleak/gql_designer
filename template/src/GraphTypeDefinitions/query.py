import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .template import (
        template_page
    )
    from .FacilityGQLModel import (
        facility_page
    )