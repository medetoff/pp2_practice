import re
a = input()
if (re.search(r"dog|cat", a)):
    print("Yes")
else:
    print("No")
