# 1) Keep only even numbers
a = [1, 2, 3, 4, 5, 6]
print(list(filter(lambda x: x % 2 == 0, a)))  # [2, 4, 6]

# 2) Keep only numbers greater than 10
b = [5, 12, 8, 20, 3, 15]
print(list(filter(lambda x: x > 10, b)))  # [12, 20, 15]

# 3) Keep only strings with length > 4
c = ["hi", "apple", "cat", "banana", "dog"]
print(list(filter(lambda s: len(s) > 4, c)))  # ['apple', 'banana']

# 4) Keep only positive numbers
d = [-5, 3, -1, 0, 7, 10, -2]
print(list(filter(lambda x: x > 0, d)))  # [3, 7, 10]

# 5) Keep only strings that start with 'a'
e = ["apple", "banana", "avocado", "cherry", "apricot"]
print(list(filter(lambda s: s.startswith("a"), e)))  # ['apple', 'avocado', 'apricot']