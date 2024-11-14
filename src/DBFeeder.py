import os
import json
import datetime
import uuid
from uoishelpers.feeders import ImportModels

from src.DBDefinitions import (
    GQLFieldModel,GQLTypeModel,GQLPossibleTypeRelationModel
    )


def readJsonFile(jsonFileName):
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if (key in ["startdate", "enddate", "lastchange", "created"]) or (key.endswith("_date")):
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                
                json_dict[key] = dateValueWOtzinfo
            
            if (key in ["id", "changedby", "createdby", "rbacobject"]) or ("_id" in key):
                
                if key == "outer_id":
                    json_dict[key] = value
                elif value not in ["", None]:
                    try:
                        json_dict[key] = uuid.UUID(value)
                    except:
                        print(f"ERROR {key} : {value}", flush=True)
                else:
                    print(key, value)

        return json_dict

    with open(jsonFileName, "r", encoding="utf-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

def get_demodata(filename="./systemdata.json"):
    return readJsonFile(filename)

async def initDB(asyncSessionMaker, filename="./systemdata.json"):

    DEMODATA = os.environ.get("DEMODATA", None) in ["True", "true"]    
    if DEMODATA:
        dbModels = [
            GQLTypeModel,GQLFieldModel,GQLPossibleTypeRelationModel
        ]
    else:
        dbModels = [GQLTypeModel,GQLFieldModel,GQLPossibleTypeRelationModel]

    jsonData = get_demodata(filename=filename)
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass