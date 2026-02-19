def fibonacci(m):
    a, b = 0, 1
    for _ in range(m):
        yield a
        a, b = b, a + b

m = int(input())
print(",".join(map(str, fibonacci(m))))