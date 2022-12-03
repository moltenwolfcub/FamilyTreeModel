def flatMap(values: list, f: 'function') -> list:
    returnlist = []
    for i in values:
        x = f(i)
        if x is not None:
            if type(x) is list:
                returnlist.extend(x)
            else:
                returnlist.append(x)
    return returnlist
