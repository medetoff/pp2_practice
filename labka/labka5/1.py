import re
s=input()
m=re.findall("^Hello",s)
if m:
    print("Yes")
else:
    print("No")