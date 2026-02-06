# 1) Class with one method
class Greeter:
    def say_hello(self):
        return "Hello!"

g = Greeter()
print(g.say_hello())


# 2) Class with method using attributes
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return "Hi, " + self.name

p = Person("Alice")
print(p.greet())


# 3) Class with two methods
class Calculator:
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

c = Calculator()
print(c.add(10, 3))
print(c.sub(10, 3))


# 4) Class with method that changes state
class Counter:
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1

cnt = Counter()
cnt.inc()
cnt.inc()
print(cnt.value)


# 5) Class with method that returns calculation
class Circle:
    def __init__(self, r):
        self.r = r

    def area(self):
        return 3.14159 * self.r * self.r

circle = Circle(3)
print(circle.area())