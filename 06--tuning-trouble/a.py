from util import consecutives

for i, (a,b,c,d) in enumerate(consecutives(open('in').read(), 4)):
    if len({a,b,c,d}) == 4:
        print(i+4)
        break
