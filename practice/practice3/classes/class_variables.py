# 1) Simple class variable
class Counter:
    count = 0

    def __init__(self):
        Counter.count += 1

a = Counter()
b = Counter()
c = Counter()
print(Counter.count)


# 2) Class variable shared by all objects
class Student:
    school = "High School"

    def __init__(self, name):
        self.name = name

s1 = Student("Alice")
s2 = Student("Bob")
print(s1.school, s2.school)


# 3) Changing class variable
class Car:
    wheels = 4

print(Car.wheels)
Car.wheels = 3
print(Car.wheels)


# 4) Instance variable vs class variable
class Dog:
    species = "Animal"

    def __init__(self, name):
        self.name = name

d1 = Dog("Rex")
d2 = Dog("Max")
print(d1.species, d2.species)


# 5) Using class variable as counter
class User:
    total_users = 0

    def __init__(self):
        User.total_users += 1

u1 = User()
u2 = User()
u3 = User()
print(User.total_users)