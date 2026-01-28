q=int(input())
s=0
for i in range(1,q+1):
    if q%i==0:
        s+=1
if s<=2:
    print("Yes")
else:
    print("No")        
