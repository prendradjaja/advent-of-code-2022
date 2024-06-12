import sys
import collections

from sscanf import sscanf


SIMULATION_LENGTH = 24


# TODO ._fields and getattr suggest using something other than namedtuple to represent Blueprint and Cost
Blueprint = collections.namedtuple('Blueprint', 'id ore_bot_cost clay_bot_cost obsidian_bot_cost geode_bot_cost')
Cost = collections.namedtuple('Cost', 'ore clay obsidian')


def main(path):
    lines = open(path).read().splitlines()
    blueprints = [parse(l) for l in lines]
    example_plan = {
        3: 'clay',
        5: 'clay',
        7: 'clay',
        11: 'obsidian',
        12: 'clay',
        15: 'obsidian',
        18: 'geode',
        21: 'geode',
    }
    simulate(blueprints[0], example_plan)


def parse(line):
    TEMPLATE = (
        'Blueprint %u: ' +
        'Each ore robot costs %u ore. ' +
        'Each clay robot costs %u ore. ' +
        'Each obsidian robot costs %u ore and %u clay. ' +
        'Each geode robot costs %u ore and %u obsidian.'
    )
    match = sscanf(line, TEMPLATE)
    assert match
    bid, *costs = match
    a, b, c1, c2, d1, d2 = costs
    return Blueprint(
        id = bid,
        ore_bot_cost      = Cost(a, 0, 0),
        clay_bot_cost     = Cost(b, 0, 0),
        obsidian_bot_cost = Cost(c1, c2, 0),
        geode_bot_cost    = Cost(d1, 0, d2),
    )


def simulate(blueprint, plan):
    '''
    Example plan:
    {
        3: 'clay',
    }
    '''
    robots = {
        'ore': 1,
        'clay': 0,
        'obsidian': 0,
        'geode': 0,
    }
    resources = {
        'ore': 0,
        'clay': 0,
        'obsidian': 0,
        'geode': 0,
    }
    for minute in range(1, SIMULATION_LENGTH + 1):
        print(f'\n== Minute {minute} ==')

        # Start constructing robot
        if minute in plan:
            new_bot_type = plan[minute]
            cost = getattr(blueprint, new_bot_type + '_bot_cost')
            print(f'Spend {format_cost(cost)} to start building a {new_bot_type}-collecting robot.')

            # Pay costs
            for resource in cost._fields:
                value = getattr(cost, resource)
                resources[resource] -= value
                assert resources[resource] >= 0, 'Invalid plan: Tried to spend more of a resource than was available'

        # Robots collect resources
        for bot_type, count in robots.items():
            resources[bot_type] += count
            if count:
                print(f'{count} {bot_type}-collecting robots collect {count} {bot_type}; you now have {resources[bot_type]} {bot_type}.')

        # Finish constructing robot
        if minute in plan:
            robots[new_bot_type] += 1
            print(f'The new {new_bot_type}-collecting robot is ready; you now have {robots[new_bot_type]} of them.')


def format_cost(cost):
    items = []
    for resource in cost._fields:
        value = getattr(cost, resource)
        if value > 0:
            items.append(f'{value} {resource}')
    assert len(items) <= 2
    return ' and '.join(items)


if __name__ == '__main__':
    main(sys.argv[1])
