n=input()
x=any(n)
v="aeiouAEIOU"
if any(i in v for i in n):
    print("Yes")
else:
    print("No")