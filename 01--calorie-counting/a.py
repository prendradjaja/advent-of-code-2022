f = lambda elf: sum(int(line) for line in elf.splitlines())
print(max(f(elf) for elf in open('in').read().split('\n\n')))
