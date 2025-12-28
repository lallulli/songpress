def Enumerate(obj, names):
    for number, name in enumerate(names):
        setattr(obj, name, number)
