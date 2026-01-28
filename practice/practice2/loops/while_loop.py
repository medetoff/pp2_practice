#1 Python has two primitive loop coomands: 1)While loops; 2)For loops
#2 With the while loop we can execute a set of statements as long as a condition is true.

#1 Example Print i as long as i less than 6:
i = 1
while i < 6:
  print(i)
  i += 1
  
  #2
running = True
count = 0
while running:
    print("Loop")
    count += 1
    if count == 3:
        running = False

#3
a = 10
while a >= 0:
    print(a)
    a -= 2

#4
num = 0
while num < 3:
    print("Hello")
    num += 1

#5
x = 5
while x > 0:
    print(x)
    x -= 1