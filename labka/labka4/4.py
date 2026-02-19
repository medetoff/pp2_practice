def div(a,n):
    for i in range(a, n + 1):
            yield i**2
c,m=map(int,input(). split())
for b in div(c,m):
    print(b)