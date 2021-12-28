from AoC2019.inputs import get_input
from collections import defaultdict

input_data = get_input(6)


def build_map(input_data):
    # parse:
    all_orbits = set((parent, child) for parent, child in (orbit.split(')') for orbit in input_data))
    print(all_orbits)

    # build graph:
    orbits_by_parent = defaultdict(list)
    # and for part 2 a reverse-lookup:
    parent_by_child = defaultdict(lambda: None)


    for orbit in all_orbits:
        orbits_by_parent[orbit[0]].append(orbit[1])
        parent_by_child[orbit[1]] = orbit[0]
    return orbits_by_parent, parent_by_child


def count_all_descendants(orbit_map, key, depth=0):
    if len(orbit_map[key]) == 0:
#        print(f'{key}: {depth} (self)')
        return depth
    else:
        accum = depth  # Count self
        # and descendents
        accum += sum((count_all_descendants(orbit_map, child, depth+1) for child in orbit_map[key]))
#        print(f'{key}: {accum} (self + children')
        return accum


# for part 2:
def get_path_to_node(parent_by_child, child):
    path = [child]
    next = child
    while True:
        parent = parent_by_child[next]
        if parent:
            path.append(parent)
            next = parent
        else:
            break
    return reversed(path)



# part 1:
# traverse from root:

# test data:
"""
                         YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
"""
#input_data = ["COM)B", "B)G", "G)H", "B)C", "C)D", "D)I", "D)E", "E)J", "J)K", "K)L", "E)F", "I)SAN", "K)YOU"]

all_orbits, parents_by_child = build_map(input_data)
print(all_orbits)

print(count_all_descendants(all_orbits, 'COM'))

# part 2:
path_to_YOU = list(get_path_to_node(parents_by_child, "YOU"))
path_to_SAN = list(get_path_to_node(parents_by_child, "SAN"))

print(path_to_YOU)
print(path_to_SAN)

# assumption - valid data so all paths start at COM
# also assumption: we can mangle these lists without consequence
# so just strip off common ancestors until we diverge.
while path_to_YOU.pop(0) == path_to_SAN.pop(0):
    pass

print(path_to_YOU)
print(path_to_SAN)

# since we've removed the shared parent, we can just count the # of asteroids on this branch
# (as a count of hops that will implicitly count the hop from this subset back to the shared parent)
total_hops = len(path_to_YOU) + len(path_to_SAN)
print(total_hops)













