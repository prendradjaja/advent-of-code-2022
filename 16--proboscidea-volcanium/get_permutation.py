def get_permutation(seq, indices):
    items = list(seq)
    result = []
    for idx in indices:
        result.append(items.pop(idx))
    return tuple(result)

def get_unused(seq, indices):
    items = list(seq)
    result = []
    for idx in indices:
        result.append(items.pop(idx))
    return tuple(items)



# print(get_permutation('abc', (1,)))
# print(get_unused('abc', (1,)))
