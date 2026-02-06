# 1) Multiply each element by 2
a = [1, 2, 3, 4, 5]
print(list(map(lambda x: x * 2, a)))

# 2) Square each number
b = [1, 2, 3, 4, 5]
print(list(map(lambda x: x ** 2, b)))

# 3) Convert strings to uppercase
c = ["hello", "python", "world"]
print(list(map(lambda s: s.upper(), c)))

# 4) Add 10 to each number
d = [5, 10, 15, 20]
print(list(map(lambda x: x + 10, d)))

# 5) Get length of each string
e = ["apple", "banana", "kiwi", "strawberry"]
print(list(map(lambda s: len(s), e)))