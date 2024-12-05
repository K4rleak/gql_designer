import sys
import asyncio
import inspect
import typing
import types
import strawberry

from strawberry.tools import create_type as create_strawberry_type

from .designerMutations import create_field, create_type , create_arg, arg_remove, type_remove, field_remove,type_remove,arg_update,field_update,type_update,generate_python_code
from ..Dataloaders import getLoadersFromContext

async def loadSchema(*, context):
    # loads from database types, their fields, recognize query and mutation
    schema_loader = getLoadersFromContext(context=context).SchemaModel
    type_loader = getLoadersFromContext(context=context).TypeModel
    dbrows = await schema_loader.filter_by(name="demoschema")
    schema = next(dbrows, None)
    assert schema is not None
    types = await type_loader.filter_by(schema_id=schema.id)
    type_array = [
        {
            "id": t.id,
            "name": t.name
        }
        for t in types
    ]
    query_type = next(filter(lambda item: item["id"] == schema.query_type_id, type_array), None)
    mutation_type = next(filter(lambda item: item["id"] == schema.mutation_type_id, type_array), None)
    return {
        "queryType": query_type,
        "mutationType": mutation_type,
        "types": type_array
    }

async def loadTypeDefinition(*, context, name):
    type_loader = getLoadersFromContext(context=context).TypeModel
    field_loader = getLoadersFromContext(context=context).FieldModel

    dbrows = await type_loader.filter_by(name=name)
    dbrow = next(dbrows, None)

    type_definition = {
        "id": dbrow.id,
        "name": dbrow.name,
        "kind": dbrow.kind
    }

    field_rows = await field_loader.filter_by(master_type_id=type_definition["id"])
    type_definition["fields"] = [
        {
            "id": field.id,
            "name": field.name,
        }
        for field in field_rows
    ]
    
    return type_definition

async def loadFieldDefinition(*, context, typename, name):

    # dataloadery
    type_loader = getLoadersFromContext(context=context).TypeModel
    field_loader = getLoadersFromContext(context=context).FieldModel
    param_loader = getLoadersFromContext(context=context).InputValueModel

    # ziskat typ, k nemuz field patry
    dbrows = await type_loader.filter_by(name=typename)
    dbrow = next(dbrows, None)
    assert dbrow is not None

    type_definition = {
        "id": dbrow.id,
        "name": dbrow.name
    }
    # print(f"param_annotations: {type_definition}")

    # nahrat z db field
    field_rows = await field_loader.filter_by(master_type_id=type_definition["id"], name=name)
    field_row = next(field_rows, None)
    assert field_row is not None

    # ziskat navratovy typ pro field
    return_type = await type_loader.load(field_row.oftype_id)

    # nahrat ty parametry, ktere patri k teto field
    params = await param_loader.filter_by(field_id=field_row.id)
    # ziskat nazvy a id typu parametru
    params_ = {param.name: param.oftype_id for param in params}
    # print(f"params_: {params_}")

    # pripravit hromadny dotaz do db pres dataloader
    futures = (type_loader.load(id) for name, id in params_.items())
    # ziskat typy
    types = await asyncio.gather(*futures)
    # usporadat to do dict a pouzit jako anotaci parametru
    param_annotations = {param_name: typing.ForwardRef(type_.name) for param_name, type_ in zip(params_.keys(), types)}

    result = {**param_annotations, "return": typing.ForwardRef(return_type.name)}
    # print(f"param_annotations: {result}")
    return result


async def createType(*, context, name, typedef):
    
    async def hello(self)-> str:
        return "hello"    

    loadedType = None # typedef
    if loadedType is None:
        loadedType = await loadTypeDefinition(context=context, name=name)

    fieldnames = [
        field["name"]
        for field in loadedType["fields"]
    ]
    fieldfutures = [
        createFieldResolver(typename=name, name=field["name"])
        for field in loadedType["fields"]
    ]
    fieldvalues = await asyncio.gather(*fieldfutures)
    fields = {
        name: {"func": value, "description": ""}
        for name, value in zip(fieldnames, fieldvalues)
    }

    # annotations = [f.__annotations__ for f in fields.values()]
    # print(f"createType {name} >> annotations: {annotations}", flush=True)
    # print(f"createType {name} >> annotations: {hello.__annotations__}", flush=True)

    strawberry_fields = [
        strawberry.field(f.func, description=fields[name].get("description", "missing description"))
        for name, f in fields.items()
    ]
    if len(strawberry_fields) == 0:
        strawberry_fields = [strawberry.field(hello, description="dummy for empty types")]
    # basetype = type(name, [], fields)
    # print(fields)

    result = create_strawberry_type(name=name, fields=strawberry_fields, is_input=loadedType["kind"]=="INPUT_OBJECT", description=loadedType.get("description", None))
    this = sys.modules[__name__]
    setattr(this, result.__name__, result)
    return 

async def createQuery(*, context, queryName, typedef):
    @strawberry.field(description="")
    async def hello(self) -> str:
        return f"hello"

    futurefields = [
        createFieldResolver(context=context, typename=queryName, name=field["name"])
        for field in typedef["fields"]
    ]

    fields = await asyncio.gather(*futurefields)

    annotations = [f.__annotations__ for f in fields]
    print(f"createQuery {queryName} >> annotations: {annotations}", flush=True)

    strawberryfields = [
        strawberry.field(field) 
        for field in fields
    ]
    if len(strawberryfields) == 0:
        strawberryfields.append(hello)

    return create_strawberry_type(name=queryName, fields=strawberryfields, description=typedef.get("description", None))


def redefine_function_signature(new_params, new_return_annotation):
    """
    Redefines the signature of the given function with new parameters and annotations.

    Parameters:
    - func: The original function to modify.
    - new_params: A list of tuples, where each tuple contains the name, default value, and annotation of a parameter.
    - new_return_annotation: The new return annotation for the function.
    """
    def wrapper(func):
    # Extract the function's existing code object and globals
        code = func.__code__
        globals_ = func.__globals__

        # Create a new parameter list for the signature
        parameters = [
            inspect.Parameter(
                name=name,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=default if default is not None else inspect.Parameter.empty,
                annotation=annotation if annotation is not None else inspect.Parameter.empty
            )
            for name, default, annotation in new_params
        ]

        # Create a new signature object
        new_signature = inspect.Signature(parameters, return_annotation=new_return_annotation)

        # Update the function's signature and annotations
        func.__signature__ = new_signature
        func.__annotations__ = {
            name: annotation for name, _, annotation in new_params if annotation is not None
        }
        if new_return_annotation is not None:
            func.__annotations__['return'] = new_return_annotation

        # Create a new function with the updated signature
        new_func = types.FunctionType(code, globals_, func.__name__)
        new_func.__signature__ = new_signature
        new_func.__annotations__ = func.__annotations__
        new_func.__doc__ = func.__doc__
        return new_func
    return wrapper

async def createFieldResolver(*, context, typename, name):

    # Attach annotations to the function
    field_definition = await loadFieldDefinition(context=context, typename=typename, name=name)
    return_annotation = field_definition.get("return", None)
    params_annotation = [("self", None, None)] + [
        (name, None, t)
        for name, t in field_definition.items()
        if name != "return"
    ]
    # params_annotation = [("self", None, None), ("id", None, typing.ForwardRef("str"))]

    @redefine_function_signature(new_params=params_annotation, new_return_annotation=return_annotation)
    async def dynamic_function(*args, **kwargs):
        return None

    # Set the function name
    dynamic_function.__name__ = name

    # print(f"createFieldResolver {name} ->> dynamic_function.__signature__: {dynamic_function.__signature__}")
    # print(f"createFieldResolver {name} ->> dynamic_function.__annotations__: {dynamic_function.__annotations__}")

    return dynamic_function

async def createMutation(*, context, mutationName, typedef):
    fields = [
        create_type,
        create_field,
        create_arg,
        arg_remove,
        type_remove,
        field_remove,
        arg_update,
        field_update,
        type_update,
        generate_python_code
    ]
    
    return create_strawberry_type(name=mutationName, fields=fields)

async def createSchema(context):
    schemaDefinition = await loadSchema(context=context)
    queryName = schemaDefinition["queryType"]["name"]
    mutationName = schemaDefinition["mutationType"]["name"]

    types = schemaDefinition["types"]
    typeIndex = {
        t["name"]: await loadTypeDefinition(context=context, name=t["name"])
        for t in types
    }
    # print(list(typeIndex.keys()), flush=True)
    strawberryInputs = {
        name: await createType(context=context, name=name, typedef=typedef)
        for name, typedef in typeIndex.items() 
        if typedef["kind"] in ["INPUT_OBJECT"]
    }

    strawberryTypes = {
        name: await createType(context=context, name=name, typedef=typedef)
        for name, typedef in typeIndex.items() 
        if (not name in [queryName, mutationName]) and (not name in strawberryInputs)
    }
    
    innerTypes = list(strawberryTypes.values())
    # print(list(strawberryTypes.keys()), flush=True)
    strawberryTypes[queryName] = await createQuery(context=context, queryName=queryName, typedef=typeIndex[queryName])
    strawberryTypes[mutationName] = await createMutation(context=context, mutationName=mutationName, typedef=typeIndex[mutationName])
    
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
    
