import uuid
import datetime
import strawberry
from typing import Annotated,ForwardRef

def TypeNameResolver(typemodel):  
    if typemodel.kind=="SCALAR":
        #print("typename_Resolver:",typemodel.id,typemodel.name, typemodel.kind,typemodel,flush=True)  
        type_map={
            "String":str,
            "DateTime": datetime.datetime,
            "UUID":uuid.UUID,
            "Int":int,
            "Boolean":bool
        }
        #print(f"TypeNameResolver Debug: id={typemodel.id}, name={typemodel.name}, kind={typemodel.kind}", flush=True)
        typemodel_type=type_map.get(typemodel.name, None)
        assert typemodel_type is not None,f"Nemam typ v mapovaci{typemodel.name}"
        return typemodel_type
    else:
        print(f"Typenamresolver return ForwardRef_{typemodel.name},{typemodel.id}")
        #return Annotated[typemodel.name,strawberry.lazy(".empty")]
        return ForwardRef(typemodel.name)
        # return typemodel.name