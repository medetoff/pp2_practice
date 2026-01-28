n = int(input())
a = list(map(int, input().split()))
q = max(a)

for i in range(len(a)):
    if a[i] == q:
        print(i + 1)
        break