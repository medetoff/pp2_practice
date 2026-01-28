#1 With the break statement we can stop the loop even if the while condition is true:
#1 Example Exit the loop when is 3:
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1
  
  #2
x = 0
while x < 10:
    if x == 5:
        break
    print(x)
    x += 1

#3
while True:
    print("Start")
    break

#4
num = 10
while num > 0:
    if num == 6:
        break
    print(num)
    num -= 1

#5
count = 0
while count < 5:
    print("Loop")
    count += 1
    if count == 2:
        break