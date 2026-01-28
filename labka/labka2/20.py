import sys
n = int(sys.stdin.readline())
d = {}
for i in range(n):
    c = sys.stdin.readline().split()
    if c[0] == "set":
        d[c[1]] = c[2]
    else:
        k = c[1]
        print(d[k] if k in d else f"KE: no key {k} found in the document")