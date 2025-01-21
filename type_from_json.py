from uuid6 import uuid7
import json

# Původní JSON text
original_data = {
    "name": "createdby",
    "description": "Who created entity",
    "args": [],
    "type": {
    "__typename": "__Type",
    "kind": "OBJECT",
    "name": "UserGQLModel",
    }
}

# Předdefinovaná hodnota master_type_id
MASTER_TYPE_ID = "019482b0-0335-7f02-83e4-9a62f77b4afa"


oftype_mapping = {
    "UUID": "01943a92-e483-7053-9483-2c16f2deb39c",
    "String":"019487b7-b92d-7a80-b1a6-4f40c9112954",
    "UserGQLModel":"1111"
}

def transform_data(data):
    
    new_id = str(uuid7())

    # Extrakce jména z původního datového typu
    name = data["type"].get("ofType", {}).get("name", "") if  data["type"].get("ofType", {}).get("name", "") else "skrr"

    
    transformed_data = {
        "id": new_id,
        "name": data["name"],
        "description": data["description"],
        "master_type_id": MASTER_TYPE_ID,
        "oftype_id": oftype_mapping.get(name, "")  # Získání oftype_id z mapování
    }

    return transformed_data

# Transformace dat
new_data = transform_data(original_data)

# Výstup
print("{\n    " + ",\n    ".join(f'\"{key}\": \"{value}\"' for key, value in new_data.items()) + "\n},")