class Pair:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def f(self,other):
        return Pair(self.x+other.x, self.y+other.y)
x1,y1,x2,y2=map(int,input().split())
p1=Pair(x1,y1)
p2=Pair(x2,y2)
r=p1.f(p2)
print(f"Result: {r.x} {r.y}")