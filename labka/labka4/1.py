def square(n):
    for i in range(1, n+1):
        yield i**2

m=int(input())        
for b in square(m):
    print(b)