def main():
    res = 0
    for line in open('in').read().splitlines():
        l, r = line.split(',')
        l = parse(l)
        r = parse(r)
        if overlaps(l, r):
            res += 1
    print(res)

def parse(pair):
    l, r = pair.split('-')
    l = int(l)
    r = int(r)
    return l,r

def overlaps(x, y):
    # TODO Implement this using just the endpoints maybe. I think contains()
    # is needed for that. Also I'm pretty sure I've done this already for past
    # AOC problems.
    return bool(set(range(x[0], x[1]+1)) & set(range(y[0], y[1]+1)))

if __name__ == '__main__':
    main()
