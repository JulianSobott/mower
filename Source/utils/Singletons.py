"""
@author: Julian
@brief: Class to inherit as metaclass, to create a Singleton class
@description:
A object from a Singleton class is only created once. Every time the constructor is called again,
the previous created object is returned.

class Example(metaclass=Singleton):

    def __init__(self):
        print("__init__")

"""


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
