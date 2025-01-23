import json
from uuid6 import uuid7

# Load JSON data
with open("schema_uois.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Get the `types` array
types = json_data["data"]["__schema"]["types"]

# List of keys you want to print
keys_to_print = ["name", "kind", "description"]

for item in types:
    new_id = str(uuid7())
    # Filter and print only the keys you care about
    filtered_item = {key: value for key, value in item.items() if key in keys_to_print and value is not None}
    
    # Print the filtered item
    print(
        "{\n    " + "id:" +",\n    ".join(f'\"{key}\": \"{value}\"' for key, value in filtered_item.items()) + "\n},"
    )

# Iterace přes každý `type`
# for type_item in types:
#     type_name = type_item.get("name", "Unknown")
#     type_kind = type_item.get("kind", "Unknown")
#     description = type_item.get("description", "No description")
    
#     print(
#         "{\n    " + ",\n    ".join(f'\"{key}\": \"{value}\"' for key, value in item.items()) + "\n},"
#     )

#     print(f"Type Name: {type_name}")
#     print(f"Kind: {type_kind}")
#     print(f"Description: {description} \n")

    # Zpracování `fields`, pokud existují
    # fields = type_item.get("fields", [])
    # for field in fields:
    #     field_name = field.get("name", "Unknown")
    #     field_type = field.get("type", {})
    #     field_type_name = field_type.get("name", "No type")
    #     oftype = field_type.get("ofType", {})
    #     oftype_name = oftype.get("name", "No ofType")
        
    #     print(f"  Field Name: {field_name}")
    #     print(f"  Type Name: {field_type_name}")
    #     print(f"  OfType Name: {oftype_name}")
    # print("-" * 40)
