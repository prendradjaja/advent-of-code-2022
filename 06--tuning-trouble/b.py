from util import consecutives

for i, chars in enumerate(consecutives(open('in').read(), 14)):
    if len(set(chars)) == 14:
        print(i+14)
        break
