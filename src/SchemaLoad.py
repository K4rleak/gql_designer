import json

def loadSchema():
    
    data = {}
    filename = "./schema.json"
    filename = "./schemameta.json"
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    data = data["data"]
    __schema = data["__schema"]
    __schema["name"] = "Schema"
    analysed = analyseSchema(__schema)

    types = [ 
        t
        for t in analysed.values() 
        if t["__typename"] == "__Type"
    ]
    print(types, flush=True)

    __typenames = set()
    kinds = set()
    for t in analysed.values():
        __typename = t["__typename"]
        __typenames.add(__typename)
        kind = t.get("kind", None)
        if kind is not None:
            kinds.add(kind)

    print(__typenames, flush=True)
    print(kinds, flush=True)

    db = {}
    for t in analysed.values():
        tablename = t["__typename"]
        table = db.get(tablename, None)
        if table is None:
            table = {}
            db[tablename] = table
        if tablename not in ["__Type", "__InputValue", "__Directive"]:
            continue
        name = t["name"]
        table[name] = cutdict(t)
    print(db)
    table = db["__Type"]
    for name, row in table.items():
        print(row)

    
def cutdict(d):
    result = {}
    for key, value in d.items():
        if isinstance(value, dict):
            continue
        elif isinstance(value, list):
            continue
        result[key] = value
    return result

def analyseSchema(schema):
    def iterateList(l):
        assert isinstance(l, list)

        for item in l:
            assert isinstance(item, dict)
            iterateDict(item)

    
    def iterateDict(leaf):
        assert isinstance(leaf, dict)
        for key, value in leaf.items():
            if isinstance(value, dict):
                iterateDict(value)
            elif isinstance(value, list):
                iterateList(value)

        if "__typename" in leaf:
            assert "name" in leaf, f"{leaf}"
            name = leaf["name"]
            record = entityIndex.get(name, None)
            if record is None:
                record = {**leaf}
                entityIndex[name] = record
            else:
                assert record["name"] == name
                record = {**record, **leaf}

    entityIndex = {}
    iterateDict(schema)
    return entityIndex
