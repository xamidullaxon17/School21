N_x = input().split()
N = int(N_x[0])
x0 = float(N_x[1])

coeffs = []
for _ in range(N + 1):
    c = float(input())
    coeffs.append(c)

# Hosila hisoblash
result = 0.0
degree = N
for coef in coeffs:
    if degree > 0:
        result += degree * coef * (x0 ** (degree - 1))
    degree -=1

print("%.3f" % result)


# input:  formula: P(x)=5x**2 + 1.2x − 3
# 2 3.0
# 5
# 1.2
# -3


