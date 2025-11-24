# Pascal's triangle

s = input()

if not s.isdigit() or int(s) <= 0:
    print("Natural number was expected")
else:
    n = int(s)
    triangle = []
    for i in range(n):
        row = [1]
        for j in range(1, i):
            row.append(triangle[i - 1][j - 1] + triangle[i - 1][j])
        if i > 0:
            row.append(1)
        triangle.append(row)

    for row in triangle:
        print(" ".join(str(x) for x in row))


# input: 
# 5