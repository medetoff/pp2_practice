import re
a = input()
m = re.findall(r"\b\w{3}\b", a)
print(len(m))
