import strawberry
from strawberry.tools import create_type as create_strawberry_type
from .designerMutations import create_field, create_type
from ..Dataloaders import getLoadersFromContext
async def loadSchema(*, context):
    # loads from database types, their fields, recognize query and mutation
    loader = getLoadersFromContext(context=context).SchemaModel
    return {
        "queryType": {
            "name": "Query",
        },
        "mutationType": {
            "name": "Mutation",
        },
        "types": [
            {
                "name": "Query",
                "fields": []
            },
            {
                "name": "Mutation",
                "fields": []
            }
        ]
    }

async def loadTypeDefinition(*, context, name):
    loader = getLoadersFromContext(context=context).TypeModel
    dbrows = await loader.filter_by(name=name)
    dbrow = next(dbrows, None)
    result = {
        "name": name,
        "fields": []
    }
    return result

async def loadFieldDefinition(*, context, typename, name):
    param_annotations = {}
    return_annotation = None
    return {**param_annotations, "return": return_annotation}


async def createType(*, context, name, typedef):
    
    async def hello(self)-> str:
        return "hello"    

    loadedType = typedef
    if loadedType is None:
        loadedType = await loadTypeDefinition(context=context, name=name)

    fields = [
        strawberry.field(
            createFieldResolver(typename=name, name=field["name"]), description=field.get("description", None))
        for field in loadedType["fields"]
    ]
    if len(fields) == 0:
        fields = [strawberry.field(hello, description="dummy for empty types")]

    # basetype = type(name, [], fields)
    # print(fields)
    return create_strawberry_type(name=name, fields=fields, description=loadedType.get("description", None))

async def createQuery(*, context, name, typedef):
    @strawberry.field(description="")
    async def hello(self) -> str:
        return f"hello"

    fields = [
        strawberry.field(
            createFieldResolver(context=context, typename=name, name=field["name"]), description=field.get("description", None))
        for field in typedef["fields"]
    ]
    if len(fields) == 0:
        fields.append(hello)

    return create_strawberry_type(name=name, fields=fields, description=typedef.get("description", None))

async def createFieldResolver(*, context, typename, name):
    async def dynamic_function(**kwargs):
        return None

    # Set the function name
    dynamic_function.__name__ = name

    # Attach annotations to the function
    dynamic_function.__annotations__ = loadFieldDefinition(context=context, typename=typename, name=name)

    return dynamic_function

async def createMutation(*, context, mutationName, typedef):
    fields = [
        create_type,
        create_field
    ]
    
    return create_strawberry_type(name=mutationName, fields=fields)

async def createSchema(context):
    schemaDefinition = await loadSchema(context=context)
    queryName = schemaDefinition["queryType"]["name"]
    mutationName = schemaDefinition["mutationType"]["name"]

    types = schemaDefinition["types"]
    typeIndex = {
        t["name"]: t
        for t in types
    }
    # print(list(typeIndex.keys()), flush=True)
    strawberryTypes = {
        name: await createType(context=context, name=name, typedef=typedef)
        for name, typedef in typeIndex.items() 
        if not name in [queryName, mutationName]
    }
    
    innerTypes = list(strawberryTypes.values())
    # print(list(strawberryTypes.keys()), flush=True)
    strawberryTypes[queryName] = await createQuery(context=context, name=queryName, typedef=typeIndex[queryName])
    strawberryTypes[mutationName] = await createMutation(context=context, name=mutationName, typedef=typeIndex[mutationName])
    
    # strawberryTypes = {
    #     typename: strawberry.type(t)
    #     for typename, t in typeIndex.items()
    # }
    query = strawberryTypes[queryName]
    mutation = strawberryTypes[mutationName]
    strawberryTypes = list(strawberryTypes.values())
    schema = strawberry.Schema(
        query=query,
        mutation=mutation,
        types=innerTypes
    )

    return schema
    
