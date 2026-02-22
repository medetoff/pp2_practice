def even_generator(n):
    for i in range(0, n + 1, 2):
        yield i

n = int(input())

first = True
for x in even_generator(n):
    if first:
        print(x, end='')
        first = False
    else:
        print(',', x, sep='', end='')
print()