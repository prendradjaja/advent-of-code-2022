import sys
import ast
import a as part_1


MIN = -1
MAX = 23


def main(path):
    sys.setrecursionlimit(16000)
    cubes = {ast.literal_eval(line) for line in open(path).read().splitlines()}
    assert (0, 0, 0) not in cubes

    exterior = flood_fill(cubes, (0, 0, 0))
    solid = invert(exterior)
    answer = part_1.solve(solid)

    print(answer)


def flood_fill(cubes, origin, result=None):
    '''
    Given a set of CUBES and ORIGIN, perform a flood fill, returning a new set (disjoint from CUBES)
    representing the filled volume.

    2D example: CUBES is #, ORIGIN is @

    . . . . .
    @ . # # .
    . # . # .
    . # # # .
    . . . . .

    Return value is X

    X X X X X
    @ X # # X
    X # . # X
    X # # # X
    X X X X X
    '''
    if result is None:
        result = set()
    result.add(origin)
    for pos in neighbors(origin):
        if not in_bounds(pos):
            continue
        if pos in result:
            continue
        if pos in cubes:
            continue
        flood_fill(cubes, pos, result)
    return result


def invert(cubes):
    result = {
        (x, y, z)
        for x in range(MIN, MAX+1)
        for y in range(MIN, MAX+1)
        for z in range(MIN, MAX+1)
    }
    for each in cubes:
        result.remove(each)
    return result


def in_bounds(cube):
    x, y, z = cube
    return (
        MIN <= x <= MAX and
        MIN <= y <= MAX and
        MIN <= z <= MAX
    )


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
