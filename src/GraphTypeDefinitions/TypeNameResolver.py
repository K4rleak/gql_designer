import uuid
import datetime

def TypeNameResolver(typemodel):  
    if typemodel.kind=="SCALAR":
        type_map={
            "String":str,
            "DateTime": datetime.datetime,
            "UUID":uuid.UUID,
            "Int":int,
            "Boolean":bool
        }
        typemodel_type=type_map.get(typemodel.name, None)
        assert typemodel_type is not None,f"Nemam typ v mapovaci{typemodel.name}"
        return typemodel_type
    else:
        return typemodel.name