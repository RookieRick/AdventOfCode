# Cribbed from 2019 since it seemed to work well enough there..
# Might feel cute later and refactor into a single shared cross-year "get_input" thing..  or might not.

# hacky constants for formats:
FLAT_LIST = 0
STRING_PER_LINE = 1
CSV_INT = 2
FLAT_LIST_INT = 3


def get_input(day: int):
    raw_formats = {1: STRING_PER_LINE,}
    parsed_formats = {1: FLAT_LIST_INT,}
    input_filename = f"./raw_inputs/day{day}.txt"
    input_file = open(input_filename, "r")

    raw_format = raw_formats[day]
    parsed_format = parsed_formats[day]
    if raw_format is STRING_PER_LINE:
        if parsed_format is FLAT_LIST:
            return [line.rstrip() for line in input_file]
        elif parsed_format is FLAT_LIST_INT:
            return [int(line.rstrip()) for line in input_file]
    elif raw_format is CSV_INT and parsed_format is FLAT_LIST:
        return [int(x) for x in input_file.read().split(',')]





