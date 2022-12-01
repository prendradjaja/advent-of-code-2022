f = lambda elf: sum(int(line) for line in elf.splitlines())
elves = sorted(f(elf) for elf in open('in').read().split('\n\n'))
print(sum(elves[-3:]))
