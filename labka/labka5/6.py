import re
s = input()
m = re.search(r'\S+@\S+\.\S+', s)
if m==None:
    print("No email")
else:
    print(m.group())