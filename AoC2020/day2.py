from AdventOfCode.AoC2020.inputs import get_input


if __name__ == "__main__":
    input = get_input(2)

    # part 1:

    valid_passwords = []
    invalid_passwords = []

    for line in input:
        parsed_policy = line[0].split('-')
        min = int(parsed_policy[0])
        max = int(parsed_policy[1])
        char = line[1]
        if line[2].count(char) < min or line[2].count(char) > max:
            invalid_passwords.append(line[2])
        else:
            valid_passwords.append(line[2])
    print(f"{len(valid_passwords)} valid, {len(invalid_passwords)} invalid")

    # part 2

    valid_passwords = []
    invalid_passwords = []

    for line in input:
        parsed_policy = line[0].split('-')
        pos1 = int(parsed_policy[0]) - 1
        pos2 = int(parsed_policy[1]) - 1
        char = line[1]
        password = line[2]
        if (password[pos1] == char and password[pos2] != char) or (password[pos1] != char and password[pos2] == char):
            valid_passwords.append(password)
        else:
            invalid_passwords.append(password)
    print(f"{len(valid_passwords)} valid, {len(invalid_passwords)} invalid")



    print("fin.")
