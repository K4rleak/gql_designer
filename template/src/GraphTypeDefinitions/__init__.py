from .query import Query
from .mutation import Mutation
schema = strawberry.federation.Schema(
    query=Query, 
    extensions=[]
)

from uoishelpers.schema import WhoAmIExtension, ProfilingExtension, PrometheusExtension
schema.extensions.append(WhoAmIExtension)