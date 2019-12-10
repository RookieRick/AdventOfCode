from AdventOfCode.AoC2019.inputs import get_input
from collections import defaultdict

input_data = get_input(6)


def build_map(input_data):
    # parse:
    all_orbits = set((parent, child) for parent, child in (orbit.split(')') for orbit in input_data))
    print(all_orbits)

    # build graph:
    orbits_by_parent = defaultdict(list)


    for orbit in all_orbits:
        orbits_by_parent[orbit[0]].append(orbit[1])
    return orbits_by_parent


def count_all_descendants(orbit_map, key, depth=0):
    if len(orbit_map[key]) == 0:
        print(f'{key}: {depth} (self)')
        return depth
    else:
        accum = depth  # Count self
        # and descendents
        accum += sum((count_all_descendants(orbit_map, child, depth+1) for child in orbit_map[key]))
        print(f'{key}: {accum} (self + children')
        return accum


# part 1:
# traverse from root:

# test data:
"""
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I
"""

all_orbits = build_map(input_data)
print(all_orbits)

print(count_all_descendants(all_orbits, 'COM'))




