def flatMap(values: list, f: 'function') -> list:
    returnlist = []
    for i in values:
        x = f(i)
        if x is not None:
            returnlist.append(x)
    return returnlist
