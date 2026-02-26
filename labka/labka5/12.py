import re
a=input()
m=re.findall(r"\d{2,}", a)
print(*m)