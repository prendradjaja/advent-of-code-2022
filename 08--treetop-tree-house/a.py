import sys

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def main():
    global HEIGHT, WIDTH
    grid = open('in').read().splitlines()
    HEIGHT = len(grid)
    WIDTH = len(grid[0])

    answer = sum(
        1
        for r in range(HEIGHT)
        for c in range(WIDTH)
        if is_visible(grid, (r, c))
    )
    print(answer)

def is_visible(grid, pos):
    return any(is_visible_from(grid, pos, d) for d in DIRECTIONS)

def is_visible_from(grid, pos, direction):
    tree = get(grid, pos)
    pos = addvec(pos, direction)
    while in_bounds(pos):
        if get(grid, pos) >= tree:
            return False
        pos = addvec(pos, direction)
    return True

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
