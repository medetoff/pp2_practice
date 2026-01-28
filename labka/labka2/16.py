v=int(input())
a=list(map(int,input().split()))
b=[]
for i in a:
    if i not in b:
        print("YES")
        b.append(i)
    else:
        print("NO")