#1 If you have only one statement to execute, you can put it on the same line as the if statement.

#1 Example One-line if statement:
a = 5
b = 2
if a > b: print("a is greater than b")

#2 If you have one statement for if and one for else, you can put them on the same line using a conditional expression:
#2 Example One-line if/else that prints a value:
a = 2
b = 330
print("A") if a > b else print("B")

#3 You can also use a one-line if/else to choose a value and assign it to a variable:
#3 Example 
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)

#4 Example Finding the maximum of two numbers:
x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)

#5 Setting a default value
username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)