#1 In programming you often need to know if an expression is True or False
#1 example
print(10 > 9)
print(10 == 9)
print(10 < 9)
#2 The bool() function allows you to evaluate any value, and give you True or False in return,

#2 example
print(bool("Hello"))
print(bool(15))
 
#3 example: Evaluate two variables
x = "Hello"
y = 15

print(bool(x))
print(bool(y))

#4 The following will return True:
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#5 The following will return False:
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})