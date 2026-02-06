# To create a class, use the keyword class:

#1 Create a class named MyClass, with a property named x:
class Myclass:
    x=5
    
#2 We can use the class named  Myclass to create objects:
p1=Myclass()
print(p1.x)

# You can delete objects by using the del keyword:
#3 Delete the p1 object:
del p1

#4 Create the 3 objects from the Myclass class:
p1=Myclass()
p2=Myclass()
p3=Myclass()

print(p1.x)
print(p2.x)
print(p3.x)

#5 The class definitions cannot be empty, but if you for some reason have a class definition with no content, put in the pass statement to avoid getting an error:
class Person:
    pass
