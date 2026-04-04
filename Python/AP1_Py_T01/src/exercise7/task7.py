N, M = map(int, input().split())

field = []
for _ in range(N):
    row = list(map(int, input().split()))
    field.append(row)

dp = [[0] * M for _ in range(N)]

dp[0][0] = field[0][0]

for j in range(1, M):
    dp[0][j] = dp[0][j-1] + field[0][j]

for i in range(1, N):
    dp[i][0] = dp[i-1][0] + field[i][0]

for i in range(1, N):
    for j in range(1, M):
        dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + field[i][j]

print(dp[N-1][M-1])



# input:
# 3 4
# 3 0 2 1
# 6 4 8 5
# 3 3 6 0