import math

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

d_A = math.sqrt(x1*x1 + y1*y1)
d_B = math.sqrt(x2*x2 + y2*y2)

direct = math.sqrt((x2-x1)**2 + (y2-y1)**2)

dx = x2 - x1
dy = y2 - y1
a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - R*R

blocked = False
if a > 1e-12:
    discriminant = b*b - 4*a*c
    if discriminant >= 0:
        sqrt_d = math.sqrt(discriminant)
        t1 = (-b - sqrt_d) / (2*a)
        t2 = (-b + sqrt_d) / (2*a)
        if t2 > 1e-9 and t1 < 1 - 1e-9:
            blocked = True

if not blocked:
    print(f"{direct:.10f}")
else:
    alpha_A = math.atan2(y1, x1)
    alpha_B = math.atan2(y2, x2)
    
    theta_A = math.acos(min(1, R / d_A)) if d_A > R else 0
    theta_B = math.acos(min(1, R / d_B)) if d_B > R else 0
    
    tan_len_A = math.sqrt(max(0, d_A*d_A - R*R))
    tan_len_B = math.sqrt(max(0, d_B*d_B - R*R))
    
    def arc_length(b1, b2):
        diff = abs(b1 - b2)
        while diff > math.pi:
            diff = abs(2 * math.pi - diff)
        return R * diff
    
    # Path 1: A's CCW tangent to B's CW tangent
    beta1_1 = alpha_A - theta_A
    beta2_1 = alpha_B + theta_B
    path1 = tan_len_A + arc_length(beta1_1, beta2_1) + tan_len_B
    
    # Path 2: A's CW tangent to B's CCW tangent
    beta1_2 = alpha_A + theta_A
    beta2_2 = alpha_B - theta_B
    path2 = tan_len_A + arc_length(beta1_2, beta2_2) + tan_len_B
    
    print(f"{min(path1, path2):.10f}")