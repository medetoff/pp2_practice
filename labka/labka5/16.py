import re
s =input()
match=re.search(r'Name: (.+), Age: (.+)' , s)
print(match.group(1), match.group(2))
