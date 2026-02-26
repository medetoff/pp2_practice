import re
s=input()
a=input()
m=re.escape(a)
b=re.findall(m,s)
print(len(b))