def _parse(tokens):
    x, *xs = tokens
    if x[0] in '0123456789':
        return (int(x), xs)
    assert x == '['
    result = []
    while xs:
        if xs[0] == ']':
            xs = xs[1:]
            break
        item, xs = _parse(xs)
        result.append(item)
    return (result, xs)

print(_parse("1".split()))
print(_parse("1 2".split()))
print(_parse("[ ]".split()))
print(_parse("[ 1 ]".split()))
print(_parse("[ 1 2 ]".split()))
print(_parse("[ 1 2 3 ]".split()))
print(_parse("[ 1 2 3 ] 4 5".split()))
print(_parse("[ 1 [ 2 3 ] 4 [ ] ]".split()))
