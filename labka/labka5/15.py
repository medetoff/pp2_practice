import re
s = input()
x=re.sub(r"\d", lambda m: m.group()*2,s)
print(x)