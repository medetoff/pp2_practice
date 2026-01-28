#1 With the break statement we can stop the loop before it has looped through all the items:
#2 Example: Exit the loop when x is "banana":
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break

#3 Example: Exit the loop when x is "banana", but this time the break comes before the print:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

#3
for ch in "hello":
    if ch == "l":
        break
    print(ch)

#4
for i in range(10):
    if i > 5:
        break
    print(i)

#5
for x in range(1, 10):
    if x == 7:
        break
    print(x)