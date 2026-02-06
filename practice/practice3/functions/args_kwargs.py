# By default, a function must be called with the correct number of arguments.
# However, sometimes you may not know how many arguments that will be passed into your function.
# *args and **kwargs allow functions to accept a unknown number of arguments.

# Arbitrary Arguments - *args
# If you do not know how many arguments will be passed into your function, add a * before the parameter name.
# This way, the function will receive a tuple of arguments and can access the items accordingly:
#1Using *args to accept any number of arguments:
def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")

#2The *args parameter allows a function to accept any number of positional arguments.
# Inside the function, args becomes a tuple containing all the passed arguments:
def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("Emil", "Tobias", "Linus")

#3
def my_function(greeting, *names):
  for name in names:
    print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus")


# Arbitrary Keyword Arguments - **kwargs
# If you do not know how many keyword arguments will be passed into your function, add two asterisks ** before the parameter name.
# This way, the function will receive a dictionary of arguments and can access the items accordingly:
#4Using **kwargs to accept any number of keyword arguments:
def my_function(**kid):
  print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes")

#5 The **kwargs parameter allows a function to accept any number of keyword arguments.
# Inside the function, kwargs becomes a dictionary containing all the keyword arguments:
def my_function(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function(name = "Tobias", age = 30, city = "Bergen")

#6
def my_function(username, **details):
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)

my_function("emil123", age = 25, city = "Oslo", hobby = "coding")