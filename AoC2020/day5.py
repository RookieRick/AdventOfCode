import AdventOfCode.AoC2020.input_parser as parser
import re
from collections import namedtuple

ValidationRule = namedtuple("ValidationRule", ["regex", "groups_validator"])

if __name__=="__main__":
    data = parser.parse("./raw_inputs/day5.txt")

    max_seat_id = 0
    seat_ids = []

    for line in data:
        row_code = line[0:7].replace("F", "0").replace("B", "1")
        seat_code = line[-3:].replace("L", "0").replace("R", "1")

        row = int(row_code, 2)
        seat = int(seat_code, 2)
        seat_id = row * 8 + seat
        seat_ids.append(seat_id)
        print(seat_id)

    print(f"MAX seat_id: {max(seat_ids)}")

    seat_ids.sort()
    my_seat = None
    for i in range(1, len(seat_ids)):
        if seat_ids[i-1] + 1 != seat_ids[i]:
            my_seat = seat_ids[i-1] + 1
            continue

    print(f"My seat: {my_seat}")

    print("fin.")