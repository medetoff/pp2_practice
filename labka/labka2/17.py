v=int(input())
w=[]
for i in range(1,v+1):
    w.append(input())
s=0
for i in w:
    if w.count(i)==3:
        s+=1
        w.remove(i)
print(s)    