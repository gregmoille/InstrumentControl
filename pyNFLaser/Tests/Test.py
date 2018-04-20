import numpy as np

def Float(fun):
    def wrap(*args, **kwargs):
        return float(fun(*args, **kwargs))
    return wrap

def Str(fun):
    def wrap(*args, **kwargs):
        return str(fun(*args, **kwargs)) + 'coucou'
    return wrap

def Bool(fun):
    def wrap(*args, **kwargs):
        return bool(fun(*args, **kwargs))
    return wrap


@float
def test1(value):
    return value

@Str
def test2(value):
    return value

@Bool
def test3(value):
    return value

if __name__ == "__main__":
    print('Test Float')
    print(test1(1))
    print('Test String')
    print(test2(1))
    print('Test Boolean ')
    print(test3(2))