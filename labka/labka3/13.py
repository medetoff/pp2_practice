q=list(map(int, input().split()))
p=lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))
w = list(filter(p, q))
if w:
    print(*w)
else:
    print("No primes")