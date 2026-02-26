import re
s=input()
m=re.findall(r'\d{2}/\d{2}/\d{4}', s)
print(len(m))