s = input()

if not s:
    print("Error: invalid input")
    exit()

allowed = "0123456789.-"
for c in s:
    if c not in allowed:
        print("Error: invalid input")
        exit()

if s.count(".") > 1 or s.count("-") > 1:
    print("Error: invalid input")
    exit()

if "-" in s and not s.startswith("-"):
    print("Error: invalid input")
    exit()

if "." in s:
    parts = s.split(".")
    if len(parts) != 2:
        print("Error: invalid input")
        exit()
    whole, frac = parts
else:
    whole = s
    frac = ""

if (whole == "" or whole == "-") and frac == "":
    print("Error: invalid input")
    exit()

sign = -1 if whole.startswith("-") else 1
whole_digits = whole.lstrip("-")
if whole_digits == "":
    w = 0
else:
    w = 0
    for ch in whole_digits:
        if ch < "0" or ch > "9":
            print("Error: invalid input")
            exit()
        w = w * 10 + (ord(ch) - ord("0"))

f = 0.0
if frac != "":
    pow10 = 1.0
    for ch in frac:
        if ch < "0" or ch > "9":
            print("Error: invalid input")
            exit()
        pow10 /= 10
        f += (ord(ch) - ord("0")) * pow10

number = sign * (w + f)
result = number * 2

print("%.3f" % result)




# input: 
# -14.97