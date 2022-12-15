def _parse(tokens):
    x, *xs = tokens
    if x[0] in '0123456789':
        return (int(x), xs)
    assert x == '['
    return _parse_exprlist(xs)

def _parse_exprlist(tokens):
    x, *xs = tokens
    if x == ']':
        return ([], xs)
    else:
        parsedX, xs = _parse(tokens)
        parsedXs, xs = _parse_exprlist(xs)
        return ([parsedX] + parsedXs, xs)

print(_parse("1".split()))
print(_parse("1 2".split()))
print(_parse("[ ]".split()))
print(_parse("[ 1 ]".split()))
print(_parse("[ 1 2 ]".split()))
print(_parse("[ 1 2 3 ]".split()))
print(_parse("[ 1 2 3 ] 4 5".split()))
print(_parse("[ 1 [ 2 3 ] 4 [ ] ]".split()))
