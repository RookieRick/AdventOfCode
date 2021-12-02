import AdventOfCode.util.input_parser as parser


if __name__=="__main__":
    data = parser.parse("./raw_inputs/day2.txt", transforms=[parser.Split()])

    # part 1
    horizontal = 0
    depth = 0
    for move in data:
        if move[0] == "forward":
            horizontal += int(move[1])
        else:
            multiplier = -1 if move[0] == "up" else 1
            depth += (multiplier * int(move[1]))

    print(horizontal * depth)

    # part 2
    horizontal = 0
    depth = 0
    aim = 0
    for move in data:
        if move[0] == "forward":
            horizontal += int(move[1])
            depth += int(move[1]) * aim
        else:
            multiplier = -1 if move[0] == "up" else 1
            aim += (multiplier * int(move[1]))

    print(horizontal * depth)
