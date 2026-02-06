# 1) Using super() to call parent __init__
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Student("Alice", 95)
print(s.name, s.grade)


# 2) Using super() to call parent method
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return super().speak() + " and Bark"

d = Dog()
print(d.speak())


# 3) Extending parent method
class Vehicle:
    def move(self):
        return "Moving"

class Car(Vehicle):
    def move(self):
        return super().move() + " fast"

c = Car()
print(c.move())


# 4) super() in multi-level inheritance
class A:
    def hello(self):
        return "Hello from A"

class B(A):
    def hello(self):
        return super().hello() + " and B"

class C(B):
    def hello(self):
        return super().hello() + " and C"

x = C()
print(x.hello())


# 5) super() with attributes
class Shape:
    def __init__(self, name):
        self.name = name

class Circle(Shape):
    def __init__(self, name, r):
        super().__init__(name)
        self.r = r

c = Circle("Circle", 3)
print(c.name, c.r)