def rev(s):
    for i in range(len(s) - 1, -1, -1):
        yield s[i]

m = input()
print("".join(rev(m))) 