# A function is a block of code which only runs when it is called.
# A function can return data as a result.
# A function helps avoiding code repetition.

#1 In Python, a function is defined using the def keyword, followed by a function name and parentheses:
def my_function():
  print("Hello from a function")

#2 To call a function, write its name followed by parentheses:
def my_function():
  print("Hello from a function")
my_function()

#3 Valid function names:
calculate_sum()
_private_function()
myFunction2()

#4 With functions - reusable code:
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

#5 Function definitions cannot be empty. If you need to create a function placeholder without any code, use the pass statement:
def my_function():
  pass
