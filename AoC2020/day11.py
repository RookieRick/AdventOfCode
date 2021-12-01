import AdventOfCode.util.input_parser as parser
import copy

DEBUG = False


def _debug(msg):
    if DEBUG:
        print(msg)


def _count_adjacent(seat_map, row, col, value, max_dist=1):
    map_min, map_max = _get_map_extents(seat_map)
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    result = 0
    max_dist = 99999999 if max_dist is None else max_dist

    for delta in deltas:
        i = row
        j = col
        for step in range(1, max_dist+1):
            i += delta[0]
            j += delta[1]
            if (i not in range(map_min[0], map_max[0])) or (j not in range(map_min[1], map_max[1])):
                break
            elif seat_map[i][j] == '.':
                pass
            else:
                result += 1 if seat_map[i][j] == value else 0
                break
    return result


def _get_map_extents(map):
    map_min = (0, 0)  # row, col
    map_max = (len(map), len(map[0]))
    return map_min, map_max


def main():
    filename = f"./raw_inputs/day11{'_debug' if DEBUG else ''}.txt"
    # we could map these to e.g., True/False/None but having them as-is is easier for
    # visualizing amd comparing debug printouts to provided examples

    for part in (1, 2):
        seat_map = parser.parse(filename, transforms=[parser.Map({"#": "#", "L": "L", ".": "."})])

        map_min, map_max = _get_map_extents(seat_map)

        if DEBUG:
            print()
            for row in seat_map:
                print(''.join(row))

        while True:
            seat_map_working_copy = copy.deepcopy(seat_map)
            for i in range(map_min[0], map_max[0]):
                for j in range(map_min[1], map_max[1]):
                    if seat_map[i][j] != ".":
                        adjacent = _count_adjacent(seat_map, i, j, "#", max_dist=1 if part == 1 else None)
                        if seat_map[i][j] == "#" and adjacent >= (4 if part == 1 else 5):
                            seat_map_working_copy[i][j] = "L"
                        elif seat_map[i][j] == "L" and adjacent == 0:
                            seat_map_working_copy[i][j] = "#"

            if DEBUG:
                print()
                for row in seat_map_working_copy:
                    print(''.join(row))

            if seat_map_working_copy == seat_map:
                break
            else:
                seat_map = copy.deepcopy(seat_map_working_copy)

        occupied = sum(row.count("#") for row in seat_map)
        print(f"part {part}: {occupied} seats occupied")

    print("fin.")


if __name__ == "__main__":
    main()


