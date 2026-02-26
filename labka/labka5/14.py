import re
s = input()
x = re.compile(r"^\d+$")
if x.match(s):
    print("Match")
else:
    print("No match")