import sys
import math

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def main():
    global HEIGHT, WIDTH
    grid = open('in').read().splitlines()
    HEIGHT = len(grid)
    WIDTH = len(grid[0])

    answer = max(
        scenic_score(grid, (r, c))
        for r in range(HEIGHT)
        for c in range(WIDTH)
    )
    print(answer)

def scenic_score(grid, pos):
    return math.prod(viewing_distance(grid, pos, d) for d in DIRECTIONS)

def viewing_distance(grid, pos, direction):
    tree = get(grid, pos)
    pos = addvec(pos, direction)
    result = 0
    while in_bounds(pos):
        result += 1
        if get(grid, pos) >= tree:
            break
        pos = addvec(pos, direction)
    return result

def in_bounds(pos):
    r, c = pos
    return (
        0 <= r < HEIGHT and
        0 <= c < WIDTH
    )

def addvec(v, w):
    return (
        v[0] + w[0],
        v[1] + w[1],
    )

def get(grid, pos):
    r, c = pos
    return grid[r][c]

if __name__ == '__main__':
    main()
