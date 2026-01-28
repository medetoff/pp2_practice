n = int(input())
w =[]
for i in range(n):
    w.append(input())
f=[]
for i in range(n):
    word= w[i]
    a=False
    for j in f:
        if j[0]==word:
            a= True
            break
    if not a:
        f.append((word, i+1))
f.sort()
for i,j in f:
    print(i, j)