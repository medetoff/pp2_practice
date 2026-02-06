# 1) Simple multiple inheritance
class A:
    def hello(self):
        return "Hello from A"

class B:
    def world(self):
        return "World from B"

class C(A, B):
    pass

c = C()
print(c.hello(), c.world())


# 2) Two parents with same method name
class X:
    def speak(self):
        return "Speak from X"

class Y:
    def speak(self):
        return "Speak from Y"

class Z(X, Y):
    pass

z = Z()
print(z.speak())  # Uses method from X because of MRO


# 3) Using super() with multiple inheritance
class A1:
    def greet(self):
        return "A1"

class B1:
    def greet(self):
        return "B1"

class C1(A1, B1):
    def greet(self):
        return super().greet()

c1 = C1()
print(c1.greet())  # Follows MRO


# 4) Combining attributes from two parents
class Fly:
    def __init__(self):
        self.can_fly = True

class Swim:
    def __init__(self):
        self.can_swim = True

class Duck(Fly, Swim):
    def __init__(self):
        Fly.__init__(self)
        Swim.__init__(self)

d = Duck()
print(d.can_fly, d.can_swim)


# 5) Method from both parents
class MathA:
    def add(self, a, b):
        return a + b

class MathB:
    def mul(self, a, b):
        return a * b

class MathC(MathA, MathB):
    pass

m = MathC()
print(m.add(2, 3), m.mul(2, 3))