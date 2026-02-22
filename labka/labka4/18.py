line1 = input().split()
x1, y1 = float(line1[0]), float(line1[1])

line2 = input().split()
x2, y2 = float(line2[0]), float(line2[1])

x_p = (x1 * y2 + x2 * y1) / (y1 + y2)
y_p = 0.0

print(f"{x_p:.10f} {y_p:.10f}")