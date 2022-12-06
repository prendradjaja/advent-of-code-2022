from util import consecutives

for i, (a,b,c,d,e, f,g,h,l,j, z,x,y,w) in enumerate(consecutives(open('in').read(), 14)):
    if len({a,b,c,d,e, f,g,h,l,j, z,x,y,w}) == 14:
        print(i+14)
        exit()
