#1 With the continue statement we can stop the current iteration of the loop, and continue with the next:

#1 Example Don't print banana:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

  #2
for num in range(1, 6):
    if num % 2 == 0:
        continue
    print(num)

#3
for ch in "python":
    if ch == "o":
        continue
    print(ch)

#4
for i in range(10):
    if i < 5:
        continue
    print(i)

#5
for x in [1, 2, 3, 4, 5]:
    if x == 3:
        continue
    print(x)