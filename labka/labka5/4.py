import re
s=input()
m=re.findall(r"\d",s)
print(*m)