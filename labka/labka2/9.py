q=int(input())
a=list(map(int,input().split()))
w=min(a)
e=max(a)
for i in a:
    if i==e:
        print(w,end=" ")
    else:
        print(i,end=" ")