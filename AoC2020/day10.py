import AdventOfCode.AoC2020.input_parser as parser
import re
from collections import defaultdict

DEBUG = False


def _debug(msg):
    if DEBUG:
        print(msg)


if __name__=="__main__":
    filename = f"./raw_inputs/day10{'_debug' if DEBUG else ''}.txt"
    adapters = parser.parse(filename, transforms=[parser.Cast(int)])

    adapters.sort()
    diffs = defaultdict(lambda: 0)
    diffs[adapters[0] - 0] += 1

    # initial diff already captured in list init
    for i in range(1, len(adapters)):
        diffs[adapters[i] - adapters[i-1]] += 1

    diffs[3] += 1  # for the device built-in

    part1 = diffs[1] * diffs[3]
    print(part1)

    # part 2 - realizing now this was a graph problem, for the sake of neatness going to just rebuild from scratch
    # instead of trying to shoe-horn into the "build a list of diffs and count" approach of part 1

    neighbors = defaultdict(lambda: list())  # use voltage val as key
    for i in range(-1, len(adapters)):  # let -1 correspond to the original outlet with val of 0
        val = 0 if i == -1 else adapters[i]
        # only need to check the next 3 for any given node:
        neighbors[val] = [candidate for candidate in adapters[i+1:i+5] if candidate - val <= 3]

    neighbors[adapters[-1]] = [adapters[-1] + 3]  # prob don't need this as it doesn't add potential paths but w/e

    # defining traverse function inline so it's painfully clear we don't need to pass the whole graph around,
    # it's "global" as far as this func is concerned:
    # we have a graph that is directed, acyclical and for which there is a path from start to finish that touches
    # every node..
    # DFS to compute "path to end" from a given node should give us what we need?
    # but we don't want to recount every time so memoize this

    paths_to_end = defaultdict(lambda: 0)   # again,with inline func we can just ref our memos directly

    def _traverse_and_count(start_id):
        if not neighbors[start_id]:  # if no neighbors, we've reached the bottom.. this must be the last node.
            paths_to_end[start_id] = 1
        else:  # recursively f
            for neighbor in neighbors[start_id]:
                if paths_to_end[neighbor]:
                    paths_to_end[start_id] += paths_to_end[neighbor]
                else:
                    paths_to_end[start_id] += _traverse_and_count(neighbor)
        return paths_to_end[start_id]

    print(_traverse_and_count(0))

    print("fin.")





