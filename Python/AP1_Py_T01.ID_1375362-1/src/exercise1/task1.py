def main():
    num1 = input()
    num2 = input()

    v1 = [float(i) for i in num1.strip().split()]
    v2 = [float(i) for i in num2.strip().split()]

    ans = 0
    for i in range(len(v1)):
        ans += v1[i] * v2[i]
    print(ans)


if __name__ == '__main__':
    main()


# input:
# 1.0 2.0 3.0
# 4.0 5.0 6.0
