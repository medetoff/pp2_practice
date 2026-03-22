from datetime import datetime
semester = datetime.strptime(input(), "%Y-%m-%d")
exam1 = datetime.strptime(input(), "%Y-%m-%d")
exam2 = datetime.strptime(input(), "%Y-%m-%d")
exam3 = datetime.strptime(input(), "%Y-%m-%d")

print((exam1 - semester).days)
print((exam2 - semester).days)
print((exam3 - semester).days)
r"\S+@\S+\.\S+"