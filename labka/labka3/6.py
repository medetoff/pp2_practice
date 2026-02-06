class Rectangle:
    def add(self,n,m):
        return n*m
a,b=map(int,input().split()) 
calc=Rectangle()
print(calc.add(a,b))