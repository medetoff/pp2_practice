n = int(input())
a = list(map(int, input().split()))
q = int(input())
for _ in range(q):
    parts = input().split()
    op = parts[0]
    if op == "add":
        x = int(parts[1])
        f = lambda v, x=x: v + x
    elif op == "multiply":
        x = int(parts[1])
        f = lambda v, x=x: v * x
    elif op == "power":
        x = int(parts[1])
        f = lambda v, x=x: v ** x
    elif op == "abs":
        f = lambda v: abs(v)
    a = list(map(f, a))
print(*a)