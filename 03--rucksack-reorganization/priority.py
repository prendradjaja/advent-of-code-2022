'''
A few different ways of calculating priority for Advent of Code 2022 Day 3.
'''

import doctest


def priority1(c):
    '''
    >>> list(range(1, 52+1)) == [
    ...     priority1(c) for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ... ]
    True
    '''
    from string import ascii_lowercase, ascii_uppercase
    return ("_" + ascii_lowercase + ascii_uppercase).index(c)


def priority2(c):
    '''
    >>> list(range(1, 52+1)) == [
    ...     priority2(c) for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ... ]
    True
    '''
    if c.islower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 1 + 26


def priority3(c):
    '''
    >>> list(range(1, 52+1)) == [
    ...     priority3(c) for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ... ]
    True
    '''
    n = ord(c) & 0b11111  # alternatively: ord(c) % 32
    is_upper = not (ord(c) & 0b100000)  # alternatively: c.isupper()
    return n + 26 * is_upper

    # as one expression:
    # return (ord(c) & 0b11111) + 26 * (not (ord(c) & 0b100000))
    # return (ord(c) % 32) + 26 * c.isupper()


if __name__ == '__main__':
    failures, tests = doctest.testmod()
    if not failures:
        print('Pass')
