from string import ascii_lowercase, ascii_uppercase

res = 0
for line in open('in').read().splitlines():
    n = len(line) // 2
    x = line[:n]
    y = line[n:]
    z = next(iter(set(x) & set(y)))
    res += ("_" + ascii_lowercase + ascii_uppercase).index(z)

print(res)
