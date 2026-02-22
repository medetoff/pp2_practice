import math

r = float(input().strip())

line2 = input().split()
x1, y1 = float(line2[0]), float(line2[1])

line3 = input().split()
x2, y2 = float(line3[0]), float(line3[1])

dx = x2 - x1
dy = y2 - y1

a = dx * dx + dy * dy
b = 2 * (x1 * dx + y1 * dy)
c = x1 * x1 + y1 * y1 - r * r

result = 0.0

if a > 0:
    discriminant = b * b - 4 * a * c

    if discriminant >= 0:
        sqrt_d = math.sqrt(discriminant)
        t1 = (-b - sqrt_d) / (2 * a)
        t2 = (-b + sqrt_d) / (2 * a)

        t_start = max(t1, 0.0)
        t_end = min(t2, 1.0)

        if t_start < t_end:
            result = (t_end - t_start) * math.sqrt(a)

print(f"{result:.10f}")