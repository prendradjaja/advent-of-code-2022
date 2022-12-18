import sys
import ast


def main(path):
    cubes = {ast.literal_eval(line) for line in open(path).read().splitlines()}
    print(solve(cubes))


def solve(cubes):
    area = 6 * len(cubes)
    for cube in cubes:
        for other in neighbors(cube):
            if other in cubes:
                area -= 1
    return area


def neighbors(cube):
    x, y, z = cube
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


if __name__ == '__main__':
    main(sys.argv[1])
