import asyncio
from typing import Any
from inspect import isawaitable 
from collections.abc import Iterable

def Tag(name):
    def wrap(name, *children, **props):
        self_children = [*children]
        self_props = {**props}
        self_name = name
        
        async def evaluate():
            childrenlen = len(self_children)
            if childrenlen == 0:
                result = f"<{self_name} " + " ".join(f"{key}={value}" for key, value in self_props.items()) + "/>\n"
                return result

            calledchildren = [child() if callable(child) else child for child in self_children]
            indexedawaitables = {index: child for index, child in enumerate(calledchildren) if isawaitable(child)}
            evaluated = await asyncio.gather(*indexedawaitables.values())
            for index, evaluated in zip(indexedawaitables.keys(), evaluated):
                calledchildren[index] = evaluated

            result = f"<{self_name} " + " ".join(f"{key}={value}" for key, value in self_props.items()) + ">\n" + "\n".join(calledchildren) + f"\n</{self_name}>"
            print(f"children: {calledchildren}, props: {self_props}")
            print(result, "\n", "*" * 30)
            return result
        
        def call(*children: Any, **props: Any) -> Any:
            childrenlen = len(children)
            keyslen = len(props.keys())
            if (childrenlen == 0) and (keyslen == 0):
                return evaluate()
                
            if childrenlen > 0:
                self_children.extend(children)
            if keyslen > 0:
                for key, value in props.items():
                    self_props[key] = value
            return call

        childrenlen = len(children)
        keyslen = len(props.keys())
        if (childrenlen == 0) and (keyslen == 0):
            # empty tag
            return evaluate()
           
        return call

    def call(*children: Any, **props: Any) -> Any:
        return wrap(name, *children, **props)
        
    return call(name)


def Tag(name):
    def Flatten(children):
        for child in children:
            if isinstance(child, str):
                yield child
                continue
            if isinstance(child, Iterable):
                yield from Flatten(child)
                continue
            yield child
        return
    
    async def Evaluate(name, *children, **props):
        childrenlen = len(children)
        if childrenlen == 0:
            result = f"<{name} " + " ".join(f"{key}={value}" for key, value in props.items()) + "/>\n"
            return result

        calledchildren = [child() if callable(child) else child for child in Flatten(children)]
        while True:
            indexedawaitables = {index: child for index, child in enumerate(calledchildren) if isawaitable(child)}
            if len(indexedawaitables) == 0:
                break

            evaluated = await asyncio.gather(*indexedawaitables.values())
            for index, evaluated in zip(indexedawaitables.keys(), evaluated):
                calledchildren[index] = evaluated
            calledchildren = [child() if callable(child) else child for child in calledchildren]

        result = f"<{name} " + " ".join(f"{key}='{value}'" for key, value in props.items()) + ">\n" + "\n".join(calledchildren) + f"\n</{name}>"
        return result
        
    def LazyEvaluate(name, *children, **props):
        def lazyResult():
            return Evaluate(name, *children, **props)
        return lazyResult
        
    def ChildrenAndProps(*children, **props):
        localchildren = [*children]
        localprops = {**props}
        def JustChildren(*_children):
            if len(_children) == 0:
                return Evaluate(name, *localchildren, *_children, **localprops)
            else:
                localchildren.extend(_children)
                return JustChildren
            
        def JustProps(**props):
            if len(props) == 0:
                return Evaluate(name, *children, **props)
            else:
                return LazyEvaluate(name, *children, **props)

        childrenlen = len(children)
        propslen = len(props)
        if (childrenlen > 0) and (propslen > 0):
            return LazyEvaluate(name, *children, **props)
        if (childrenlen == 0) and (propslen == 0):
            return Evaluate(name=name)
        if (childrenlen == 0):
            return JustChildren
        else:
            return JustProps
        
    return ChildrenAndProps

async def asyncy():
    yield "A"
    yield "B"

async def main():
    div = Tag("div")
    span = Tag("span")

    def Page(data):
        return div(className="card")(f"{key}: {value} " for key, value in data.items())
    def Page2(data):
        return div(className="card")("A")
    def Page3(data):
        return div("A")
    async def subPage(key, value):
        return span(f"{key}: {value}")
    
    def Page4(data):
        result = div(className="card")(
            div(className="card-body")(
                subPage(key, value) for key, value in data.items()
            )
        )
        return result
    
    print("have Tag div")
    result = await div()
    print("1", result)
    result = await div("A", "B", id="main")()
    print("2", result)
    result = await div(className="card")()
    print("3", result)
    result = await div(className="card")(
        div(className="card-header")("A")
    )()
    print("4", result)
    result = await Page({"name": "John", "surname": "Newbie"})()
    print("5", result)
    result = await Page2({"name": "John", "surname": "Newbie"})()
    print("6", result)
    result = await Page3({"name": "John", "surname": "Newbie"})()
    print("7", result)
    result = await Page4({"name": "John", "surname": "Newbie"})()
    print("8", result)



    # a = asyncy()
    # print(type(a), type(a).__name__, dir(a))

print("*" * 30)
print("*" * 30)
asyncio.run(main())