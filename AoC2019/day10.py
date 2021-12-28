from AoC2019.inputs import get_input
import math
import bisect
from collections import OrderedDict

data = get_input(10)
print(data)
asteroids = set()

# assumption: input is well-formed with all lines same length
height = len(data)
width = len(data[0])

print(f"{width} x {height}")
for y in range(height):
    for x in range(width):
        if data[y][x] == '#':
            asteroids.add((x, y))

#print(asteroids)

# cheating and letting somebody else derive the math for me (https://math.stackexchange.com/questions/1596513/find-the-bearing-angle-between-two-points-in-a-2d-space)
# basically we want to find angle between every asteroid and every other..  then from any given asteroid I can "see" only one for each unique angle.

angles = {}  # map source: [(angle, (dest))]
ranked = []  #[(# visible, (source))]
for source in asteroids:
    angles[source] = []
    for other in (other for other in asteroids if other != source):
        # oh hell, our y coords are backwards from normal cartesian, so we need to reverse this vector LOL GAAAH
        # i.e., instead of substracting source from other..
        angle = math.atan2(source[0] - other[0], source[1] - other[1])
        # and because of that same bit of funkiness, we end up going counter-clockwise.. so just flip our angles
        angle = -angle
        # and finally normalize so we start our sort pointing "up"
        angle = angle if angle >= 0 else angle + 2 * math.pi  # ensure positive, will be helpful for part 2.
        angles[source].append((angle, other))
    unique = set((angle[0] for angle in angles[source]))
    ranked.append((len(unique), source))

ranked.sort()
print(ranked[-1])

source = ranked[-1][1]  # (22, 19)
targets_by_angle_by_mag = OrderedDict.fromkeys(sorted([angle[0] for angle in angles[source]]))
for key in targets_by_angle_by_mag:
    targets_by_angle_by_mag[key] = []

for target in angles[source]:
    angle, other = target
    mag = math.pow(other[0] - source[0], 2) + math.pow(other[1]- source[1], 2)
    bisect.insort(targets_by_angle_by_mag[angle], (mag, other))

num_destroyed = 0
while num_destroyed < 200:
    # loop through our angle-first map, destroy first found at each angle
    for angle, target_list in targets_by_angle_by_mag.items():
        if target_list:
            target = target_list.pop(0)
            num_destroyed += 1
            print(f"at angle {angle} destroyed #{num_destroyed}: {target} leaving {target_list}")
            if num_destroyed == 200:
                break


