# TODO I think there's probably a faster recursive solution here that avoids repeated work. Base
# case is E, which has path_length_to_e = 0. Recursive case checks neighbors, finds the minimum
# result of the subproblem for each of those, and returns that +1.
#
# At some point maybe I'll try this out...

import sys
from collections import deque


def main():
    path = sys.argv[1]
    grid = open(path).read().splitlines()

    starts = find_starts(grid)
    answer = min(solve1(grid, start) for start in starts)
    print(answer)


def solve1(grid, start, progress=None):
    search_result = bfs(grid, start)
    if search_result:
        parents, end = search_result
    else:
        return float('inf')
    node = end
    answer = 0
    while node != start:
        answer += 1
        node = parents[node]
    return answer



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


def find_starts(grid):
    HEIGHT = len(grid)
    WIDTH = len(grid[0])
    result = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if getindex(grid, (r, c)) in {'S', 'a'}:
                result.append( (r, c) )
    return result

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
