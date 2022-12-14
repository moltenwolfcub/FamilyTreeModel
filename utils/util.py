from typing import Callable, TypeVar, Sequence

T = TypeVar('T')
def flatMap(values: Sequence, f: Callable[[T], T]) -> list:
    returnlist: list[T] = []
    for i in values:
        x: T = f(i)
        if x is not None:
            if type(x) is list:
                returnlist.extend(x)
            else:
                returnlist.append(x)
    return returnlist
