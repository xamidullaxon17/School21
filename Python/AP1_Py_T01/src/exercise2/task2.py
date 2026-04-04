def main():
    n = int(input())

    if n < 0:
        print(False)
    else:
        ans = n
        num = 0
        while n != 0:
            qoldiq = n % 10
            num = num * 10 + qoldiq
            n = n // 10

        print(ans == num)

if __name__ == '__main__':
    main()



# input:
# 1143411