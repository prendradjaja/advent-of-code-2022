def _parse(tokens):
    x, *xs = tokens
    if x[0] in '0123456789':
        return (int(x), xs)
    if is_non_nested_list(tokens):
        idx = tokens.index(']')
        number_tokens = tokens[1 : idx]
        return ([int(t) for t in number_tokens], tokens[idx + 1:])
    assert x == '['
    result = []
    while xs:
        if xs[0] == ']':
            xs = xs[1:]
            break
        item, xs = _parse(xs)
        result.append(item)
    return (result, xs)

def is_non_nested_list(tokens):
    assert tokens[0] == '['
    for t in tokens[1:]:
        if t == '[':
            return False
        elif t == ']':
            return True
    raise Exception('Reached end')

print(_parse("1".split()))
print(_parse("1 2".split()))
print(_parse("[ ]".split()))
print(_parse("[ 1 ]".split()))
print(_parse("[ 1 2 ]".split()))
print(_parse("[ 1 2 3 ]".split()))
print(_parse("[ 1 2 3 ] 4 5".split()))
print(_parse("[ 1 [ 2 3 ] 4 [ ] ]".split()))
