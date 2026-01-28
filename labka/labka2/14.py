n=int(input())
a=list(map(int,input().split()))
maxc=0
c=None
for i in a:
    s=a.count(i)
    if s>maxc:
        maxc=s
        c=i
if maxc==1:
    print(min(a))
else:
    print(c)        
