from collections import namedtuple, deque
from functools import cache
from itertools import tee
import itertools
import sys

from sscanf import sscanf


Valve = namedtuple('Valve', 'id flow_rate neighbors')


def main(path):
    global all_valves
    all_valves = {}
    for line in open(path).read().splitlines():
        valve = parse_line(line)
        all_valves[valve.id] = valve

    openable_valves = [v.id for v in all_valves.values() if v.flow_rate > 0]
    assert 'AA' not in openable_valves

    example_plan = tuple(openable_valves)
    print('Example plan duration:', get_plan_duration(example_plan))

    solve_example(openable_valves)

    # CONTINUE HERE: Try implementing a backtracking solution


def solve_example(openable_valves):
    '''
    This solution works for the example input because 6! (len(openable_valves) == 6) is small, but
    won't work for the puzzle input.
    '''
    if len(openable_valves) > 10:
        return
    plans = list(itertools.permutations(openable_valves))
    assert all(is_valid_plan(plan) for plan in plans)
    print('Answer:', max(get_plan_score(plan) for plan in plans))


def parse_line(line):
    line = line.replace('to valve ', 'to valves ')
    line = line.replace('tunnel leads', 'tunnels lead')
    result = sscanf(
        line,
        'Valve %s has flow rate=%u; tunnels lead to valves %s'
    )
    assert result
    valve_id, flow_rate, neighbors_string = result
    neighbors = neighbors_string.split(', ')
    return Valve(valve_id, flow_rate, neighbors)


# TODO This overlaps a lot with get_plan_score(). Can we clean anything up?
def get_plan_duration(valves_to_open):
    time_to_open_valves = len(valves_to_open)
    travel_time = 0
    for a, b in pairwise(('AA',) + valves_to_open):
        travel_time += shortest_path(a, b)
    return time_to_open_valves + travel_time


def is_valid_plan(valves_to_open):
    return get_plan_duration(valves_to_open) < 30


def get_plan_score(valves_to_open):
    path = ('AA',) + valves_to_open
    time_elapsed = 0
    released = 0

    for a, b in pairwise(path):
        time_elapsed += 1 + shortest_path(a, b)  # Add 1 for time to open the valve

        # How much pressure will this valve release over the rest of the 30 minutes?
        released += all_valves[b].flow_rate * (30 - time_elapsed)

    return released


@cache
def shortest_path(id1, id2):
    '''
    Return the length of the shortest path from one valve to another. If there's a tunnel directly
    between them, then length is 1, etc.
    '''
    def bfs(node):
        parents = {}
        visited = set()
        visited.add(node)
        q = deque([node])
        while q:
            node = q.popleft()
            for v in neighbors(node):
                if v not in visited:
                    parents[v] = node
                    if v == id2:
                        return parents
                    visited.add(v)
                    q.append(v)
        raise Exception('No path found')
    def neighbors(node):
        valve = all_valves[node]
        return valve.neighbors

    parents = bfs(id1)
    curr = id2
    result = 0
    while curr != id1:
        result += 1
        curr = parents[curr]
    return result


# From https://docs.python.org/3/library/itertools.html#itertools.pairwise
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


if __name__ == '__main__':
    main(sys.argv[1])
