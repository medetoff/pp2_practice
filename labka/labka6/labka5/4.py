n = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))

dot_product = sum(x * y for x, y in zip(A, B))
print(dot_product)