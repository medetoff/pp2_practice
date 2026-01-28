"""
#1 Python supports the usual logical conditions from mathematics:
Equals: a == b
Not Equals: a != b
Less than: a < b
Less than or equal to: a <= b
Greater than: a > b
Greater than or equal to: a >= b
"""

#2 If statement
a = 33
b = 200
if b > a:
  print("b is greater than a")
  
#3 If statement, without indentation (will raise an error):
"""a = 33
b = 200
if b > a:
print("b is greater than a") # you will get an error
"""

#4Multiple statements in an if block:
age = 20
if age >= 18:
  print("You are an adult")
  print("You can vote")
  print("You have full legal rights")
  
  #5
is_logged_in = True
if is_logged_in:
  print("Welcome back!")