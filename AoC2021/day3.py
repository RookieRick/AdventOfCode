import AdventOfCode.util.input_parser as parser

if __name__ == "__main__":
    data = parser.parse("./raw_inputs/day3.txt")

    # there's probably a clever math trick to do this, but there's also BRUTE FORCE..
    # key assumption (which we *could* validate but not bothering to): all binary value strings are same length
    input_length = len(data[0])
    gamma = ""
    epsilon = ""
    # accumulate counts index by position within string
    ones = [0] * input_length
    zeros = [0] * input_length
    for value in data:
        for i in range(input_length):
            if value[i] == "1":
                ones[i] += 1
            else:
                zeros[i] += 1

    for i in range(input_length):
        if ones[i] > zeros[i]:
            gamma += "1"
            epsilon += "0"
        elif zeros[i] > ones[i]:
            gamma += "0"
            epsilon += "1"
        else:
            raise ValueError("problem didn't specify what to do if no clear winner....")

    gamma_val = int(gamma, 2)
    epsilon_val = int(epsilon, 2)
    power = gamma_val * epsilon_val
    print(f"power={power}")

    # part 2 - MOAR BRUTE.
    o2_gen_candidates = data.copy()
    co2_scrubber_candidates = data.copy()

    # This could prob be decomposed into function(s) and what-not but I'm several days behind after being on vacation :)

    i = 0
    # unlike in part 1, we'll use "ones" and "zeros" as more transient values, getting recomputed on each iteration
    # and only containing the result for the currently relevant bit being inspected, grouped by list being inspected
    O2_INDEX = 0
    CO2_INDEX = 1
    ones = {O2_INDEX: 0, CO2_INDEX: 0}
    zeros = {O2_INDEX: 0, CO2_INDEX: 0}
    while len(o2_gen_candidates) > 1 or len(co2_scrubber_candidates) > 1:
        if i >= input_length:
            raise ValueError("Ran out of runway. Kaboom.")

        if len(o2_gen_candidates) > 1:
            ones[O2_INDEX] = len([value for value in o2_gen_candidates if value[i] == "1"])
            zeros[O2_INDEX] = len(o2_gen_candidates) - ones[O2_INDEX]
            most_common = "1" if ones[O2_INDEX] >= zeros[O2_INDEX] else "0"
            o2_gen_candidates = [value for value in o2_gen_candidates if value[i] == most_common]

        if len(co2_scrubber_candidates) > 1:
            ones[CO2_INDEX] = len([value for value in co2_scrubber_candidates if value[i] == "1"])
            zeros[CO2_INDEX] = len(co2_scrubber_candidates) - ones[CO2_INDEX]
            least_common = "0" if zeros[CO2_INDEX] <= ones[CO2_INDEX] else "1"
            co2_scrubber_candidates = [value for value in co2_scrubber_candidates if value[i] == least_common]

        i += 1

    o2_gen_value = int(o2_gen_candidates[0], 2)
    co2_scrubber_value = int(co2_scrubber_candidates[0], 2)
    print(f"life support rating: {o2_gen_value * co2_scrubber_value}")


    print("fin.")