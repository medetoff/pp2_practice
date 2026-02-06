# 1) Simple inheritance
class Animal:
    def speak(self):
        return "Animal sound"

class Dog(Animal):
    def speak(self):
        return "Bark"

d = Dog()
print(d.speak())


# 2) Inheriting attributes
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Student("Alice", 95)
print(s.name, s.grade)


# 3) Using parent method
class Vehicle:
    def move(self):
        return "Moving"

class Car(Vehicle):
    pass

c = Car()
print(c.move())


# 4) Method overriding
class Shape:
    def area(self):
        return 0

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

r = Rectangle(4, 5)
print(r.area())


# 5) Checking inheritance with isinstance
class A:
    pass

class B(A):
    pass

b = B()
print(isinstance(b, A))