import re


def parse(filename, blob=False, transforms=None):
    # transforms should be provided in inverse order
    # for example.. to split lines based on a delimiter and cast the results to int call like:
    # parse(my_file, transforms=[Cast(int), Split(", |: ")
    # Mental model behind this decision was e.g., Cast(Split(operand))
    transforms = transforms or []
    operations = transforms[::-1]

    def inner_func(operand):
        result = operand
        for operation in operations:
            result = operation(result)
        return result

    with open(filename) as input_file:
        if blob:
            return inner_func(input_file.read().rstrip())
        else:
            return [inner_func(line.rstrip()) for line in input_file]


class Cast(object):
    # TODO: extend this to accept a LIST of types if you want to apply it after e.g., Split..
    def __init__(self, target_type):
        # target_type must be callable and accept string (e.g., int, float)
        self.target_type = target_type

    def __call__(self, operand):
        if type(operand) is str:
            return self.target_type(operand)
        else:
            # assume it's iterable
            return [self.target_type(val) for val in operand]


class Split(object):
    def __init__(self, delimiter_regex):
        self.delimiter = delimiter_regex

    def __call__(self, operand):
        if type(operand) is str:
            return re.split(self.delimiter, operand)
        else:
            # assume it's iterable
            return [re.split(self.delimiter, val) for val in operand]


class Map(object):
    def __init__(self, map_definition):
        self.map = map_definition

    def __call__(self, operand):
        # operand should be a string with only characters in the map..
        return [self.map[char] for char in operand]



