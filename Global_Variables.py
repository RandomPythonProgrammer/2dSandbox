Variables = {}


def get(variable):
    return Variables[variable]


def set(variable, value):
    Variables[variable] = value


def check_for(value):
    if value in Variables.keys():
        return True
    else:
        return False


def list():
    return Variables
