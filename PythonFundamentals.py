from abc import ABC, abstractmethod
from typing import AbstractSet


def InOut (name):
    print("Hello "+name)

def DataTypes (choice):
    match choice:
        case 1:
            x = 10
            print("int example:", x)
            print("type:", type(x))

        case 2:
            x = 3.14
            print("float example:", x)
            print("type:", type(x))

        case 3:
            x = "Hello to our system"
            print("string example:", x)
            print("type:", type(x))

        case 4:
            x = [1, 2, 3]
            print("list example:", x)
            print("type:", type(x))

        case 5:
            x = (1, 2, 3)
            print("tuple example:", x)
            print("type:", type(x))

        case 6:
            x = {"name": "Shahd", "age": 20}
            print("dictionary example:", x)
            print("type:", type(x))

        case 7:
            x = {"Hi", "Shahd" , "Hi"}
            print("Set example:", x)
            print("type:", type(x))

        case 8:
            print("Bye 👋")

        case _:
            print("Invalid choice ❌")


def Casting (x):
    print("Cast example:", x)
    print(f"{x} in integer =", int(x))
    print(f"{x} in string =", str(x))
    print(f"{x} in float =", float(x))

########### Inheritance & Polymorphism
class Animal:

    def __init__ (self):
        print("From animal class")

    def sound(self):
        print("Some animal sound")

    def _onlyFprAnimals(self):
        print("Only for animals")

class Dog(Animal):

    def __init__ (self):
        print("From dog class")

    def sound(self):           # Override func. so it's polymorphism
        print("Dog sound")


########### Abstraction
class lang(ABC):
    @abstractmethod
    def regards(self):
        pass

class Franch(lang):
    def regards(self):
        print("Salut")

########### Static
class Calc:
    @staticmethod
    def add(a, b):
        return a + b


########### ContextManager
class ContextManager:
    def __init__(self):
        print('init method ')

    def __enter__(self):
        print('enter method ')
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exit method ')

########### Decorates

def changecase(func):
  def toupper(x):
    return func(x).upper()
  return toupper

@changecase
def fun(x):
  return x





