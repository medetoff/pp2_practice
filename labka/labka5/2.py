import re
s=input()
b=input()
m=re.search(b,s)
if m:
    print("Yes")
else:
    print("No")