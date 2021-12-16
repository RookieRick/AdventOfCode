import AdventOfCode.util.input_parser as parser
from collections import defaultdict
import numpy as np

DEBUG = False

data = parser.parse(
    f"./raw_inputs/day5{'_debug' if DEBUG else ''}.txt",
    transforms=[parser.Split(","), parser.Split("->")]
)


data = np.array(data, dtype=np.int)

# part 1/2:
# take 1: brute force
for part in (1, 2):
    sparse_map = defaultdict(lambda: defaultdict(lambda: 0))
    for line in data:
        min_y = min(line[0][0], line[1][0])
        max_y = max(line[0][0], line[1][0])
        min_x = min(line[0][1], line[1][1])
        max_x = max(line[0][1], line[1][1])

        # for part 2, include any where rise == run..
        if part == 2 and (max_y - min_y) == (max_x - min_x):
            delta_x = 1 if line[0][1] == min_x else -1
            delta_y = 1 if line[0][0] == min_y else -1
            for i in range(max_y + 1 - min_y):
                sparse_map[line[0][1] + i * delta_x][line[0][0] + i * delta_y] += 1
        elif min_y == max_y or min_x == max_x:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    sparse_map[x][y] += 1

    total_count = 0
    for row in sparse_map.values():
        for col, count in row.items():
            if count >= 2:
                total_count += 1

    print(f"part {part}: {total_count}")

print("fin.")
