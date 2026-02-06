# Lambda Functions
# A lambda function is a small anonymous function.
# A lambda function can take any number of arguments, but can only have one expression.

#1 Add 10 to argument a, and return the result:
x = lambda a : a + 10
print(x(5))

#2 Multiply argument a with argument b and return the result:
x = lambda a, b : a * b
print(x(5, 6))

#3 Summarize argument a, b, and c and return the result:
x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

#4 
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))

#5
def myfunc(n):
  return lambda a : a * n

mytripler = myfunc(3)

print(mytripler(11))