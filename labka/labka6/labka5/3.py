n = int(input())
words = input().split()

result = []
for i, word in enumerate(words):
    result.append(f"{i}:{word}")

print(" ".join(result))