import AdventOfCode.AoC2020.input_parser as parser
import re
from collections import namedtuple

ValidationRule = namedtuple("ValidationRule", ["regex", "groups_validator"])

if __name__=="__main__":
    data = parser.parse("./raw_inputs/day4.txt", blob=True, transforms=[parser.Split("\n| "), parser.Split("\n\n")])

    valid = 0
    invalid = 0

    year = re.compile('^(\d{4})$')

    # dict of field key: (regex for val, validation func to operate on .groups() from regex match)
    all_fields = {
        'byr': ValidationRule(year, lambda x: 1920 <= int(x[0]) <= 2002),
        'iyr': ValidationRule(year, lambda x: 2010 <= int(x[0]) <= 2020),
        'eyr': ValidationRule(year, lambda x: 2020 <= int(x[0]) <= 2030),
        'hgt': ValidationRule(
            re.compile('^(\d+)(cm|in)$'),
            lambda x: 150 <= int(x[0]) <= 193 if x[1] == 'cm' else 59 <= int(x[0]) <= 76
        ),
        'hcl': ValidationRule(re.compile('^#[0-9|a-f]{6}$'), None),
        'ecl': ValidationRule(re.compile('^amb|blu|brn|gry|grn|hzl|oth$'), None),
        'pid': ValidationRule(re.compile('^[0-9]{9}$'), None),
        'cid': None}

    for record in data:
        fields = {k: v for k, v in [field.split(':') for field in record]}
        missing = set(all_fields.keys()) - set(fields.keys())
        if (not missing) or missing == {'cid'}:
            any_field_failed = False
            for key, rule in all_fields.items():
                if rule:
                    match = rule.regex.match(fields[key])
                    if not match or rule.groups_validator and not rule.groups_validator(match.groups()):
                        print(f"{key} failed validation for value {fields[key]}")
                        any_field_failed = True
                        continue
            if any_field_failed:
                invalid += 1
            else:
                valid += 1

    print(f"{valid} {invalid}")
    print("fin.")