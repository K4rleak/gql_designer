from functools import cache

from src.DBDefinitions import (
    SchemaModel,
    TypeModel,
    FieldModel,
)


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

import os
from uoishelpers.feeders import ImportModels

from uoishelpers.dataloaders import readJsonFile

def get_demodata(filename="./systemdata.json"):
    return readJsonFile(filename)

async def initDB(asyncSessionMaker, filename="./systemdata.json"):

    DEMODATA = os.environ.get("DEMODATA", None) in ["True", "true"]    
    if DEMODATA:
        dbModels = [
                SchemaModel,
                TypeModel,
                FieldModel,
            ]
    else:
        dbModels = [
        ]
    jsonData = get_demodata(filename=filename)
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass