n=int(input())
a=list(map(int,input().split()))
if all(i>=0 for i in a):
    print("Yes")
else:
    print("No")