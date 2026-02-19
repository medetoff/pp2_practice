def div(n):
    for i in range(0, n + 1):
        if i%3==0 and i%4==0:
            yield i

m = int(input())
for b in div(m):
    print(b)