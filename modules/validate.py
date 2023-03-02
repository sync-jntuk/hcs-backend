

def is_valid(data):
    if str(type(data)) == "<class 'str'>":
        return data.find("'") == -1
    elif str(type(data)) == "<class 'list'>" or str(type(data)) == "<class 'tuple'>":
        for d in data:
            if d.find("'") != -1:
                return False
        return True
    elif str(type(data)) == "<class 'dict'>":
        for k, v in data.items():
            if k.find("'") != -1 or v.find("'") != -1:
                return False
        return True
    else:
        return False

