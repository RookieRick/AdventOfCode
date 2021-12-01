import AdventOfCode.util.input_parser as parser

if __name__=="__main__":
    data = parser.parse("./raw_inputs/day6.txt", transforms=[parser.Split('\n'), parser.Split('\n\n')], blob=True)

    group_answers = []
    group_unanimous = []
    for group in data:
        all_yes_answers = set()
        common_yes_answers = None
        for single_answerset in group:
            yes_answers = set(iter(single_answerset))
            all_yes_answers.update(yes_answers)
            if common_yes_answers is None:
                common_yes_answers = yes_answers
            else:
                common_yes_answers.intersection_update(yes_answers)
        group_answers.append(all_yes_answers)
        group_unanimous.append(common_yes_answers)

    total_yes = sum([len(group_answer) for group_answer in group_answers])
    print(f"{total_yes}")
    total_unanimous = sum([len(group_answer) for group_answer in group_unanimous])
    print(f"{total_unanimous}")

    print("fin.")