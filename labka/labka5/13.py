import re
txt = input()
x = re.findall("\w+", txt)
print(len(x))