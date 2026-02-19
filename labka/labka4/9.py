def power(n):
    for i in range(0, n+1):
        yield 2**i

m=int(input())        
print(" ".join(map(str, power(m))))