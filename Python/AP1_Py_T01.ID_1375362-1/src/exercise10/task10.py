from itertools import combinations

first_line = input().split()
N = int(first_line[0])
required_time = int(first_line[1])

machines = []
for _ in range(N):
    year, cost, time = map(int, input().split())
    machines.append( (year, cost, time) )

years = {}
for year, cost, time in machines:
    if year not in years:
        years[year] = []
    years[year].append( (cost, time) )

min_total_cost = None

for year, lst in years.items():
    if len(lst)<2:
        continue
    for a, b in combinations(lst,2):
        total_time = a[1]+b[1]
        if total_time >= required_time:
            total_cost = a[0]+b[0]
            if (min_total_cost is None) or (total_cost < min_total_cost):
                min_total_cost = total_cost

if min_total_cost is not None:
    print(min_total_cost)
else:
    print("Error: invalid input")


# input:
# 5 48
# 2023 100 14
# 2020 18 347
# 2023 10000000 34
# 2023 1000 34
# 2022 10 34