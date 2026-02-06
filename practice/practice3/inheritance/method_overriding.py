# 1) Simple method overriding
class Animal:
    def speak(self):
        return "Animal sound"

class Cat(Animal):
    def speak(self):
        return "Meow"

c = Cat()
print(c.speak())


# 2) Overriding method with different behavior
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, a):
        self.a = a

    def area(self):
        return self.a * self.a

s = Square(4)
print(s.area())


# 3) Using super() in overridden method
class Person:
    def greet(self):
        return "Hello"

class Student(Person):
    def greet(self):
        return super().greet() + ", I am a student"

st = Student()
print(st.greet())


# 4) Overriding method that uses attributes
class Vehicle:
    def speed(self):
        return 0

class Car(Vehicle):
    def __init__(self, max_speed):
        self.max_speed = max_speed

    def speed(self):
        return self.max_speed

car = Car(180)
print(car.speed())


# 5) Overriding method and changing return type
class Printer:
    def info(self):
        return "Printer"

class ColorPrinter(Printer):
    def info(self):
        return "Color Printer"

p = ColorPrinter()
print(p.info())