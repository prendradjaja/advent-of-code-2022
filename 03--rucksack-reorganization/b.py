from string import ascii_lowercase, ascii_uppercase

def chunks(lst):
    while lst:
        yield (lst.pop(0), lst.pop(0), lst.pop(0))

res = 0
for b, c, d in chunks(open('in').read().splitlines()):
    z = next(iter(set(b) & set(c) & set(d)))
    res += ("_" + ascii_lowercase + ascii_uppercase).index(z)

print(res)
