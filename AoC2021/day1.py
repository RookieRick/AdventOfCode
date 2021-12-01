import AdventOfCode.util.input_parser as parser


if __name__=="__main__":
    data = parser.parse("./raw_inputs/day1.txt", transforms=[parser.Split('\n'), parser.Split('\n\n')], blob=True)
