a=int(input())
b=input().split()
c=input().split()
d=input()
q=dict(zip(b,c))
if d in q:
    print(q[d])
else:
    print("Not found")