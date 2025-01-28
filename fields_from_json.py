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
        "name": "externalIds",
        "description": "All related external ids",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "NON_None",
        "name": None,
        "ofType": {
            "__typename": "__Type",
            "kind": "LIST",
            "name": None,
            "ofType": {
            "kind": "NON_None",
            "name": None
            }
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
        "name": "label",
        "description": "Facility full name assigned by an administrator",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "SCALAR",
        "name": "String",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "address",
        "description": "Facility address",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "SCALAR",
        "name": "String",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "valid",
        "description": "is the facility still valid",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "SCALAR",
        "name": "Boolean",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "capacity",
        "description": "Facility's capacity",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "SCALAR",
        "name": "Int",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "geometry",
        "description": "Facility geometry (SVG)",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "SCALAR",
        "name": "String",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "geolocation",
        "description": "Facility geo address (WGS84+zoom)",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "SCALAR",
        "name": "String",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "type",
        "description": "Facility type",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "OBJECT",
        "name": "FacilityTypeGQLModel",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "eventState",
        "description": "Intermediate entity linking the event and facility",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "OBJECT",
        "name": "FacilityEventStateTypeGQLModel",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "masterFacility",
        "description": "Facility above this",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "OBJECT",
        "name": "FacilityGQLModel",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "subFacilities",
        "description": "Facilities inside facility (like buildings in an areal)",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "NON_None",
        "name": None,
        "ofType": {
            "__typename": "__Type",
            "kind": "LIST",
            "name": None,
            "ofType": {
            "kind": "NON_None",
            "name": None
            }
        }
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "group",
        "description": "Facility management group",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "OBJECT",
        "name": "GroupGQLModel",
        "ofType": None
        },
        "isDeprecated": False,
        "deprecationReason": None
    },
    {
        "name": "plannedLessons",
        "description": "planned items",
        "args": [],
        "type": {
        "__typename": "__Type",
        "kind": "NON_None",
        "name": None,
        "ofType": {
            "__typename": "__Type",
            "kind": "LIST",
            "name": None,
            "ofType": {
            "kind": "NON_None",
            "name": None
            }
        }
        },
        "isDeprecated": False,
        "deprecationReason": None
    }
    ],
}

MASTER_TYPE_ID = "0194a6be-097a-7c48-a240-29b6542a88bf"

# Mapování typů na jejich ID
oftype_mapping = {
    "UUID": "01943a92-e483-7053-9483-2c16f2deb39c",
    "String": "019487b7-b92d-7a80-b1a6-4f40c9112954",
    "UserGQLModel": "0194abb8-7c37-7a38-a1c0-9fcbf33eae54",
    "DateTime": "019487d0-ac6b-7fff-aaae-c6eab327047e",
    "Int":"0194a6c5-06e5-7d17-9cb2-34ca335aec53",
    "Boolean":"0194a6c8-02c7-7a4e-b960-b917b8427b87"

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
    oftype_id = item.get("oftype_id")
    
    #if oftype_id:
    print(
        "{\n    " + ",\n    ".join(f'\"{key}\": \"{value}\"' for key, value in item.items()) + "\n},"
    )