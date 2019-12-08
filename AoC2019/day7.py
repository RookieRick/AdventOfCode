from AdventOfCode.AoC2019.intcode import IntCodeComputer
from AdventOfCode.AoC2019.inputs import day7_parsed
from itertools import permutations

computer = IntCodeComputer(day7_parsed)
phase_sequences = list(permutations(range(0, 5)))

max_val = 0
next_input = 0

for phase_sequence in phase_sequences:
    next_input = 0
    for seq_val in phase_sequence:
        print(f"computing with seq={seq_val}, accum={next_input}")
        computer.compute([seq_val, next_input])
        next_input = computer.outputs[-1]
    max_val = max(max_val, computer.outputs[-1])

print(f"MAX: {max_val}")



