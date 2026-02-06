# 1) Sort numbers in ascending order
a = [5, 2, 9, 1, 7]
print(sorted(a, key=lambda x: x))

# 2) Sort numbers in descending order
b = [5, 2, 9, 1, 7]
print(sorted(b, key=lambda x: x, reverse=True))

# 3) Sort strings by length
c = ["apple", "kiwi", "banana", "fig", "cherry"]
print(sorted(c, key=lambda s: len(s)))

# 4) Sort list of tuples by second element
d = [(1, 3), (4, 1), (2, 2), (5, 0)]
print(sorted(d, key=lambda t: t[1]))

# 5) Sort list of dictionaries by 'age'
e = [
    {"name": "Ali", "age": 20},
    {"name": "Bob", "age": 18},
    {"name": "Chris", "age": 25},
]
print(sorted(e, key=lambda x: x["age"]))