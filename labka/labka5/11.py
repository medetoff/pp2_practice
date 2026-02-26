import re
a = input()
m = re.findall(r"[A-Z]", a)
print(len(m))
