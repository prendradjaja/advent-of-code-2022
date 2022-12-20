import sys
from dataclasses import dataclass


def main(path):
    # Parse
    lines = open(path).read().splitlines()
    lst = [WrappedInt(int(l)) for l in lines]

    # Mix
    copy = list(lst)
    for item in copy:
        value = item.value
        index = lst.index(item)
        move(lst, index, value)

    # Get answer
    [zero_index] = [i for i, item in enumerate(lst) if item.value == 0]
    answer = (
        lst[(zero_index + 1000) % len(lst)].value +
        lst[(zero_index + 2000) % len(lst)].value +
        lst[(zero_index + 3000) % len(lst)].value
    )
    print(answer)


def move(lst, index, offset):
    item = lst.pop(index)
    new_index = (index + offset) % len(lst)
    lst.insert(new_index, item)


@dataclass
class WrappedInt:
    value: int
    def __eq__(self, other):
        return self is other


if __name__ == '__main__':
    main(sys.argv[1])
