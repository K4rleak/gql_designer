from uuid6 import uuid7
import json

# Původní JSON text
original_data = {
    "fields": [
    {
        "name": "id",
        "description": "Entity primary key",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "NON_None",
        "name": None,
        "ofType": {
            "__typename": "__Type",
            "kind": "SCALAR",
            "name": "UUID",
            "ofType": None
        }
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "name",
        "description": "Name ",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "NON_None",
        "name": None,
        "ofType": {
            "__typename": "__Type",
            "kind": "SCALAR",
            "name": "String",
            "ofType": None
        }
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "nameEn",
        "description": "English name",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "NON_None",
        "name": None,
        "ofType": {
            "__typename": "__Type",
            "kind": "SCALAR",
            "name": "String",
            "ofType": None
        }
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "createdby",
        "description": "Who created entity",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "OBJECT",
        "name": "UserGQLModel",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "changedby",
        "description": "Who made last change",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "OBJECT",
        "name": "UserGQLModel",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "created",
        "description": "Time of entity introduction",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "SCALAR",
        "name": "DateTime",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "lastchange",
        "description": "Time of last update",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "NON_None",
        "name": None,
        "ofType": {
            "__typename": "__Type",
            "kind": "SCALAR",
            "name": "DateTime",
            "ofType": None
        }
        },
        "isDeprecated": False,
        "deprecationReason": None
    }
    ],
}

MASTER_TYPE_ID = "019482b0-0335-7f02-83e4-9a62f77b4afa"

# Mapování typů na jejich ID
oftype_mapping = {
    "UUID": "01943a92-e483-7053-9483-2c16f2deb39c",
    "String": "019487b7-b92d-7a80-b1a6-4f40c9112954",
    "UserGQLModel": "019487cf-65bd-724c-963a-d47215bb7486",
    "DateTime": "019487d0-ac6b-7fff-aaae-c6eab327047e"

}

def transform_data(fields):
    transformed = []
    for field in fields:
        # Generování UUIDv7 pro každý záznam
        new_id = str(uuid7())
        
        # Extrakce názvu typu (ofType nebo name)
        oftype = field["type"].get("ofType", None)
        name_value = oftype.get("name", "") if oftype else field["type"].get("name", "")
        
        # Vytvoření transformovaného záznamu
        transformed_field = {
            "id": new_id,
            "name": field["name"],
            "description": field["description"],
            "master_type_id": MASTER_TYPE_ID,
            "oftype_id": oftype_mapping.get(name_value, "")
        }
        transformed.append(transformed_field)
    return transformed

# Transformace dat
new_data = transform_data(original_data["fields"])

# Výstup
for item in new_data:
    print(
        "{\n    " + ",\n    ".join(f'\"{key}\": \"{value}\"' for key, value in item.items()) + "\n},"
    )