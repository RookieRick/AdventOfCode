import itertools
import json
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
    def __init__(self, target_types):
        # target_type must be (optionally, a list of) callable and accept string (e.g., int, float)
        if type(target_types) != list:  # assume we were handed a bare type for backward compat and dev convenience
            target_types = [target_types]

        self.target_types = target_types

    def __call__(self, operand):
        if type(operand) is str:
            return self.target_types[0](operand)
        else:
            # assume it's iterable..
            # if we don't have enough target types, reuse the last one as needed
            # also assume we should always have at least as many values as types
            if len(operand) < len(self.target_types):
                raise IndexError("Not enough values for specified types")
            return [
                target_type(val) for val, target_type in itertools.zip_longest(
                    operand, self.target_types, fillvalue=self.target_types[-1]
                )
            ]


class Split(object):
    def __init__(self, delimiter_regex="\\s"):
        self.delimiter = delimiter_regex

    def __call__(self, operand):
        if type(operand) is str:
            return re.split(self.delimiter, operand)
        else:
            # assume it's iterable
            return [re.split(self.delimiter, val) for val in operand]


class Replace(object):
    def __init__(self, pattern, replacement, count=-1):
        self.pattern = pattern
        self.replacement = replacement
        self.count = count

    def __call__(self, operand):
        if type(operand) is str:
            return operand.replace(self.pattern, self.replacement, self.count)
        else:  # assumer iterable of strings
            return [val.replace(self.pattern, self.replacement, self.count) for val in operand]


class Map(object):
    def __init__(self, map_definition):
        self.map = map_definition

    def __call__(self, operand):
        # operand should be a string with only characters in the map..
        return [self.map[char] for char in operand]


class JsonLoad(object):
    def __call__(self, operand):
        if type(operand) is str:
            return json.loads(operand)
        else:  # assume iterable of strings
            return [json.loads(val) for val in operand]


