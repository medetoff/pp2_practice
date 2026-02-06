class sal:
    def add(self,n,m):
        if n>=m:
            return n-m
        else: 
            return "Insufficient Funds"
a,b=map(int,input().split()) 
c=sal()
print(c.add(a,b))
