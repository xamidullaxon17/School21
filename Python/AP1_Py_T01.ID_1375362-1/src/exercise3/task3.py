def main():
    with open("input.txt") as f:
        lines = f.readlines()

    matrix = [list(map(int, line.strip().split())) for line in lines]
    n = len(matrix)

    visited = [[False]*n for _ in range(n)]

    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    squares = 0
    circles = 0

    def dfs(x, y, cells):
        visited[x][y] = True
        cells.append((x,y))
        for d in dirs:
            nx = x + d[0]
            ny = y + d[1]
            if 0 <= nx < n and 0 <= ny < n:
                if not visited[nx][ny] and matrix[nx][ny]==1:
                    dfs(nx, ny, cells)

    for i in range(n):
        for j in range(n):
            if matrix[i][j]==1 and not visited[i][j]:
                cells = []
                dfs(i, j, cells)
                min_x = min(c[0] for c in cells)
                max_x = max(c[0] for c in cells)
                min_y = min(c[1] for c in cells)
                max_y = max(c[1] for c in cells)
                has_zero_inside = False
                for x0 in range(min_x, max_x+1):
                    for y0 in range(min_y, max_y+1):
                        if matrix[x0][y0]==0:
                            has_zero_inside = True
                if has_zero_inside:
                    circles += 1
                else:
                    squares += 1

    print(f"{squares} {circles}")

if __name__ == "__main__":
    main()

# no input