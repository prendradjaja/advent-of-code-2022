import sys
from collections import deque


def main():
    path = sys.argv[1]
    grid = open(path).read().splitlines()

    start = find_start(grid)
    parents, end = bfs(grid, start)
    node = end
    answer = 0
    while node != start:
        answer += 1
        node = parents[node]
    print(answer)


def bfs(grid, node):
    parents = {}
    visited = set()
    visited.add(node)
    q = deque([node])
    while q:
        node = q.popleft()
        for v in neighbors(grid, node):
            if v not in visited:
                parents[v] = node
                if getindex(grid, v) == 'E':
                    return (parents, v)
                visited.add(v)
                q.append(v)
def neighbors(grid, node):
    for d in directions:
        neighbor = addvec(node, d)
        if (
            in_bounds(grid, neighbor)
            and is_ok_elevation_change(
                getindex(grid, node),
                getindex(grid, neighbor)
            )
        ):
            yield neighbor


def is_ok_elevation_change(e, f):
    if e == 'S':
        e = 'a'
    if f == 'E':
        f = 'z'
    return ord(f) - 1 <= ord(e)


def find_start(grid):
    HEIGHT = len(grid)
    WIDTH = len(grid[0])
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if getindex(grid, (r, c)) == 'S':
                return (r, c)

def in_bounds(grid, pos):
    HEIGHT = len(grid)
    WIDTH = len(grid[0])
    r, c = pos
    return (
        0 <= r < HEIGHT and
        0 <= c < WIDTH
    )


def getindex(grid, pos):
    r, c = pos
    return grid[r][c]


def addvec(v, w):
    return (
        v[0] + w[0],
        v[1] + w[1],
    )


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


if __name__ == '__main__':
    main()
