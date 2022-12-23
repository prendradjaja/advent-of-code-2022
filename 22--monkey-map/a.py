import sys


DIRECTIONS = [
    RIGHT := (0, 1),
    DOWN := (1, 0),
    LEFT := (0, -1),
    UP := (-1, 0),
]


def main(path):
    # Parse
    text = open(path).read().rstrip('\n')
    board, instructions = text.split('\n\n')
    instructions = parse_instructions(instructions)
    board = parse_board(board)


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
                next_pos = move(board, pos, heading)
                if board[next_pos] == '.':
                    pos = next_pos

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
        return next_pos
    else:  # Wrap case
        r, c = pos
        if heading == DOWN:
            r = min(R for (R, C) in board if C == c)
            return r, c
        elif heading == UP:
            r = max(R for (R, C) in board if C == c)
            return r, c
        elif heading == RIGHT:
            c = min(C for (R, C) in board if R == r)
            return r, c
        elif heading == LEFT:
            c = max(C for (R, C) in board if R == r)
            return r, c
        else:
            raise Exception('Unreachable case')


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


if __name__ == '__main__':
    main(sys.argv[1])
