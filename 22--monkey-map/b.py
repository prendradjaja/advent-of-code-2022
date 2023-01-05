'''
Usage:
    python3 b.py ex

To run coherence test:
    python3 b.py ex -t

To run coherence test in verbose mode:
    python3 b.py ex -t -v
'''

import sys
import ast
import collections


WrapDef = collections.namedtuple('WrapDef', 'heading a_to_A b_to_B')

DIRECTIONS = [
    RIGHT := (0, 1),
    DOWN := (1, 0),
    LEFT := (0, -1),
    UP := (-1, 0),
]


def main(path):
    global regions, geometry

    # Parse
    text = open(path).read().rstrip('\n')
    board, instructions = text.split('\n\n')
    instructions = parse_instructions(instructions)
    board = parse_board(board)
    regions = parse_regions(open(path + '.regions').read())
    geometry = parse_geometry(open(path + '.geometry').read())

    # Find starting location
    pos = (0, 0)
    while board.get(pos) != '.':
        pos = addvec(pos, RIGHT)

    heading = RIGHT

    # Simulate
    for each in instructions:
        if each in ['L', 'R']:
            heading = turn(heading, each)
        else:
            for _ in range(each):
                next_pos, next_heading = move(board, pos, heading)
                if board[next_pos] == '.':
                    pos = next_pos
                    heading = next_heading

    # Massage final state into answer
    r, c = pos
    answer = (
        1000 * (r + 1)
        + 4 * (c + 1)
        + DIRECTIONS.index(heading)
    )
    print(answer)


def move(board, pos, heading):
    next_pos = addvec(pos, heading)
    if board.get(next_pos):  # Non-wrap case
        next_heading = heading
        return next_pos, next_heading
    else:  # Wrap case
        r, c = pos
        heading
        region = regions[pos]
        wrap_def = geometry[region, heading]

        mapper = make_mapper(wrap_def.a_to_A, wrap_def.b_to_B)
        next_pos = mapper(pos)
        next_heading = wrap_def.heading
        return next_pos, next_heading


def turn(heading, rotation):
    offset = {
        'R': 1,
        'L': -1,
    }[rotation]
    index = DIRECTIONS.index(heading)
    return DIRECTIONS[(index + offset) % len(DIRECTIONS)]


def parse_board(raw_board):
    result = {}
    for r, row in enumerate(raw_board.splitlines()):
        for c, ch in enumerate(row):
            if ch != ' ':
                result[r,c] = ch
    return result


def parse_regions(s):
    return {
        k: int(v)
        for (k, v) in parse_board(s).items()
    }


def parse_geometry(s):
    s = s.replace('UP', str(UP))
    s = s.replace('DOWN', str(DOWN))
    s = s.replace('LEFT', str(LEFT))
    s = s.replace('RIGHT', str(RIGHT))
    result = {}
    for k, v in ast.literal_eval(s).items():
        result[k] = WrapDef(*v)
    return result


def parse_instructions(s):
    """ Returns e.g. [10, 'R', 5, 'L', ...] """
    s = s.replace('R', ' R ')
    s = s.replace('L', ' L ')
    result = []
    for word in s.split():
        try:
            word = int(word)
        except ValueError:
            pass
        result.append(word)
    return result


def addvec(v, w):
    return (
        v[0] + w[0],
        v[1] + w[1],
    )


def make_mapper(a_to_A, b_to_B):
    def is_int(n):
        EPSILON = 0.00001
        return abs(round(n) - n) < EPSILON

    def to_complex(pos):
        r, c = pos
        return r + c*1j

    def from_complex(pt):
        r = pt.real
        c = pt.imag
        try:
            assert is_int(r) and is_int(c)
        except AssertionError:
            print('No int', r, c)
            raise
        return (round(r), round(c))

    a, A = a_to_A
    b, B = b_to_B
    a = to_complex(a)
    b = to_complex(b)
    A = to_complex(A)
    B = to_complex(B)

    def map_point(pos):
        pt = to_complex(pos)
        x = (pt - a) / (b - a)
        return from_complex(A + x * (B - A))

    return map_point


def coherence_test(path, verbose):
    '''
    This test is intended to catch typos etc in the geometry and regions
    files. It's a simple sanity check: Start at some location on the cube,
    move all the way around the cube without turning, and check that you've
    returned to the same location. Repeat for every location and heading.
    '''

    def test_one(start_pos, start_heading):
        pos = start_pos
        heading = start_heading
        log('\nTesting', pos, heading)
        for _ in range(4 * n):
            pos, heading = move(board, pos, heading)
            log('- Moving', pos, heading)
        is_pass = pos == start_pos and heading == start_heading
        log(f'* Start pos & heading: {start_pos} {start_heading}')
        log(f'* Final pos & heading: {pos} {heading} (should be unchanged)')
        log('* Pass' if is_pass else f'FAIL')
        if not is_pass:
            log()
            print('At least one test failed. Stopped at first failure.')
            if not verbose:
                print('Run with -v for verbose mode.')
            exit()

    def log(*items):
        if verbose:
            print(*items)

    global regions, geometry

    # Parse
    text = open(path).read().rstrip('\n')
    board, instructions = text.split('\n\n')
    instructions = parse_instructions(instructions)
    board = parse_board(board)
    regions = parse_regions(open(path + '.regions').read())
    geometry = parse_geometry(open(path + '.geometry').read())

    if path == 'ex':
        n = 4
    elif path == 'in':
        n = 50

    text = open(path).read().rstrip('\n')
    board, _ = text.split('\n\n')
    board = board.replace('#', '.')
    board = parse_board(board)

    for pos in board:
        for heading in DIRECTIONS:
            test_one(pos, heading)
    log()
    print('All tests passed!')


if __name__ == '__main__':
    if '-t' not in sys.argv:
        main(sys.argv[1])
    else:
        # Parse args
        argv = list(sys.argv)
        argv.remove('-t')
        verbose = False
        if '-v' in argv:
            verbose = True
            argv.remove('-v')

        coherence_test(argv[1], verbose)
