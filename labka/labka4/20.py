def solve():
    m = int(input())
    
    g = 0
    n = 0
    
    for _ in range(m):
        parts = input().split()
        scope = parts[0]
        value = int(parts[1])
        
        if scope == "global":
            g += value
        elif scope == "nonlocal":
            n += value
        # local does nothing to g or n
    
    print(g, n)

solve()