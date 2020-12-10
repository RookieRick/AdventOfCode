import AdventOfCode.AoC2020.input_parser as parser
import re
from collections import defaultdict

DEBUG = False


def _debug(msg):
    if DEBUG:
        print(msg)


if __name__=="__main__":
    filename = f"./raw_inputs/day9{'_debug' if DEBUG else ''}.txt"
    data = parser.parse(filename, transforms=[parser.Cast(int)])

    preamble_length = 25 if not DEBUG else 5

    exploit = -1
    match = False
    for i in range(preamble_length, len(data)):
        preamble = data[i - preamble_length: i]
        value = data[i]
        if DEBUG:
            print(preamble)

        # brute force it first..
        match = False
        for val1 in preamble:
            for val2 in preamble:
                if val1 == val2:
                    continue
                if val1 + val2 == value:
                    match = True
                    break
            if match:
                break
        if not match:
            print(value)
            exploit = value
            break

    run_found = False
    for i in range(0, len(data)):
        for j in range(i+2, len(data)):
            if sum(data[i:j]) == exploit:
                run_found = True
                weakness = min(data[i:j]) + max(data[i:j])
                print(weakness)
                break
        if run_found:
            break


    print("fin.")


