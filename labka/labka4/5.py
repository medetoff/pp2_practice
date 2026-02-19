def count_down_to(n):
    while n >= 0:
        yield n
        n-=1
    
m=int(input())
for num in count_down_to(m):
  print(num)