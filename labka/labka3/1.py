def valid(n):
    s=str(n)
    for i in s:
        if int(i)%2!=0:
            return "Not valid"
    return "Valid"
number=int(input())
print(valid(number))
