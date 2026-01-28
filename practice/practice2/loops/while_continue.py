#1 With the continue statement we can stop the current iteration, and continue with the next:

#1 Example continue to the next iteration if i is 3:
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

#2
x = 0
while x < 6:
    x += 1
    if x % 2 == 0:
        continue
    print(x)

#3
count = 0
while count < 4:
    count += 1
    if count == 2:
        continue
    print("Hi")

#4
num = 0
while num < 7:
    num += 1
    if num > 4:
        continue
    print(num)

#5
i = 5
while i > 0:
    i -= 1
    if i == 2:
        continue
    print(i)