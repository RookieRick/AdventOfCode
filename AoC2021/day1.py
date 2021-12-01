import AdventOfCode.util.input_parser as parser


if __name__=="__main__":
    data = parser.parse("./raw_inputs/day1.txt", transforms=[parser.Cast(int)])

    # part 1
    increases = 0
    for i in range(1, len(data)):
        if data[i] > data[i-1]:
            increases += 1
    print(increases)

    # part 2

    increases = 0
    for i in range(3, len(data)):
        if sum(data[i-3:i]) > sum(data[i-4:i-1]):
            increases += 1

    print(increases)


