def main():
    res = 0
    for line in open('in').read().splitlines():
        l, r = line.split(',')
        l = parse(l)
        r = parse(r)
        if contains(l, r) or contains(r, l):
            res += 1
    print(res)

def parse(pair):
    l, r = pair.split('-')
    l = int(l)
    r = int(r)
    return l,r

def contains(small, big):
    return (
        big[0] <= small[0] and
        big[1] >= small[1]
    )

if __name__ == '__main__':
    main()
