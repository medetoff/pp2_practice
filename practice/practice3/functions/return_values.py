# Functions can return values using the return statement:
#1
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)

#2 A function that returns a list:
def my_function():
  return ["apple", "banana", "cherry"]

fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])

#3 A function that returns a tuple:
def my_function():
  return (10, 20)

x, y = my_function()
print("x:", x)
print("y:", y)

#4 You can specify that a function can have ONLY positional arguments.
# To specify positional-only arguments, add , / after the arguments:
def my_function(name, /):
  print("Hello", name)

my_function("Emil")

#5
def my_function(name):
  print("Hello", name)

my_function(name = "Emil")