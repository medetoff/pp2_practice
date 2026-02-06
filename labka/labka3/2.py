def isusual(n):
    if n<=0:
        return False
    while n%2==0: n=n//2
    while n%3==0: n=n//3
    while n%5==0: n=n//5
    
    return n==1

num=int(input())
if isusual(num):
    print("Yes")
else:
    print("No")    