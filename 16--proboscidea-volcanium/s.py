from collections import namedtuple, deque
from functools import cache
from itertools import tee
import itertools
import sys

from sscanf import sscanf
from get_permutation import get_permutation, get_unused


Valve = namedtuple('Valve', 'id flow_rate neighbors')


def main(path):
    global all_valves, max_score, openable_valve_ids
    all_valves = {}
    for line in open(path).read().splitlines():
        valve = parse_line(line)
        all_valves[valve.id] = valve

    openable_valve_ids = [v.id for v in all_valves.values() if v.flow_rate > 0]
    assert 'AA' not in openable_valve_ids

    max_score = 0
    empty_state = ()
    backtracking_search(empty_state)
    print(max_score)


def backtracking_search(state):
    global max_score
    score = get_plan_score(get_permutation(openable_valve_ids, state))
    max_score = max(max_score, score)
    for child in child_nodes(state):
        backtracking_search(child)


def child_nodes(state):
    plan = get_permutation(openable_valve_ids, state)
    unused = get_unused(openable_valve_ids, state)
    for i, each in enumerate(unused):
        child_state = state + (i,)
        child_plan = plan + (each,)
        if is_valid_plan(child_plan):
            yield child_state


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
