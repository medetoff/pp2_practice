# Information can be passed into functions as arguments.
# Arguments are specified after the function name, inside the parentheses. You can add as many arguments as you want, just separate them with a comma.
# The following example has a function with one argument (fname). When the function is called, we pass along a first name, which is used inside the function to print the full name:

#1 A function with one argument:
def my_function(fname):
  print(fname + " Refsnes")
my_function("Emil")
my_function("Tobias")
my_function("Linus")

# From a function's perspective:
# A parameter is the variable listed inside the parentheses in the function definition.
# An argument is the actual value that is sent to the function when it is called.

#2
def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument

#3 his function expects 2 arguments, and gets 2 arguments:
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")

#4 You can assign default values to parameters. If the function is called without an argument, it uses the default value:
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

#5 You can send arguments with the key = value syntax.
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(animal = "dog", name = "Buddy")

#6 You can send any data type as an argument to a function (string, number, list, dictionary, etc.).
# The data type will be preserved inside the function:
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)
