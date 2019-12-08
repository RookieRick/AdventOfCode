# day 4 - another brute force approach for starters..

min = 193651
max = 649729


def check_conditions(input_number, run_required_min = 2, run_required_max = 6):
    input_string = str(input_number)
    run_lengths = set()
    current_run = 1
    for index in range(0, len(input_string)-1):
        # decreasing digit rules out immediately
        if input_string[index+1] < input_string[index]:
            return False
        # repeated character (at least once) required:
        if input_string[index] == input_string[index+1]:
            current_run += 1
        else: # record and reset
            run_lengths.add(current_run)
            current_run = 1
    #  make sure we record our last run:
    run_lengths.add(current_run)

    # if we reach this point we didn't bail out due to decreasing
    for run_length in run_lengths:
        if run_required_min <= run_length <= run_required_max:
            return True
    return False


def main():
    #part 1:
    count = 0
    for x in range(min, max+1):
        if check_conditions(x):
            count += 1
    print(count)

    #part 2:
    count = 0
    for x in range(min, max+1):
        if check_conditions(x, 2, 2):
            count += 1
    print(count)


if __name__ == "__main__":
    main()
