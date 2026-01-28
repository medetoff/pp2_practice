#1 Get the characters from position 2 to position 5 (not included):
b = "Hello, World!"
print(b[2:5])

#2 The upper() method returns the string in upper case:
a = "Hello, World!"
print(a.upper())

#3 The lower() method returns the string in lower case:
a = "Hello, World!"
print(a.lower())

#4 The strip() method removes any whitespace from the beginning or the end:
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

#5 The replace() method replaces a string with another string:
a = "Hello, World!"
print(a.replace("H", "J"))

#6 The split() method splits the string into substrings if it finds instances of the separator:
a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']

#7 
age = 36
txt = f"My name is John, I am {age}"
print(txt)