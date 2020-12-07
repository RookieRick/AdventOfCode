import AdventOfCode.AoC2020.input_parser as parser
import re
from collections import defaultdict

if __name__=="__main__":
    data = parser.parse("./raw_inputs/day7.txt")

    can_contain = defaultdict(lambda: set())
    can_be_contained_by = defaultdict(lambda: set())
    for line in data:
        rule_components = line.split(" bags contain ")
        container_descriptor = rule_components[0]
        contained_descriptors = re.split(r"((\d) (\w+ \w+) bag[s]?[,.])+", rule_components[1])
        while len(contained_descriptors) > 4:
            del contained_descriptors[0:2]
            # populate sparse, we'll traverse recursively
            can_contain[container_descriptor].add((contained_descriptors[1], int(contained_descriptors[0])))
            can_be_contained_by[contained_descriptors[1]].add(container_descriptor)

            del contained_descriptors[0:2]

    def all_containers(target):
        result = set(can_be_contained_by[target])
        for container in can_be_contained_by[target]:
            result.update(all_containers(container))
        return result

    def count_contains(container):
        result = sum(contained[1] for contained in can_contain[container])
        print(f"{result}: {container} --> {can_contain[container]}")
        for contained in can_contain[container]:
            result += count_contains(contained[0]) * contained[1]
        return result

    part_1 = all_containers("shiny gold")
    print(len(part_1))
    print(part_1)
    part_2 = count_contains("shiny gold")
    print(part_2)

    print("fin.")