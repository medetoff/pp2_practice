"""
1 A for loop is used for 
iterating over a sequence 
(that is either a list, 
a tuple, a dictionary, a set or a string)
"""
#2 example Print each fruit in a fruit list:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  
#3 Example Loop through the letters in the word "banana":
for x in "banana":
    print(x)
    
#4 Example Exit the loop when x is "banana":
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break

#5 Example Exit the loop when x is "banana", but this time the break comes before the print:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)