# All classes have a built-in method called  __init__(), which is always executed when the class is being initiated.
#The ___init__() method is used to assign values to object properities, or to perform operations that are necessary when the object is being created.

#1 Create a class named Person, use the __init__() method to assign values for name and age:
class Person:
   def __init__(self,name ,age):
       self.name=name
       self.age=age
p1=Person("Emil",36)
print(p1.name)
print(p1.age) 

# 2) __init__ with one attribute
class Car:
    def __init__(self, brand):
        self.brand = brand

c = Car("Toyota")
print(c.brand)


# 3) __init__ with default value
class Student:
    def __init__(self, name, grade=0):
        self.name = name
        self.grade = grade

s1 = Student("Bob")
s2 = Student("Ann", 95)
print(s1.name, s1.grade)
print(s2.name, s2.grade)


# 4) __init__ doing calculation
class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.area = w * h

r = Rectangle(4, 5)
print(r.area)


# 5) __init__ with list attribute
class Box:
    def __init__(self):
        self.items = []

b = Box()
b.items.append("apple")
b.items.append("banana")
print(b.items)