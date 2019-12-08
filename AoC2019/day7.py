from AdventOfCode.AoC2019.intcode import IntCodeComputer
from AdventOfCode.AoC2019.inputs import day7_parsed
from itertools import permutations
import queue
import threading


def part1():
    computer = IntCodeComputer(day7_parsed)
    phase_sequences = list(permutations(range(0, 5)))

    max_val = 0

    for phase_sequence in phase_sequences:
        next_input = 0
        for seq_val in phase_sequence:
            print(f"computing with seq={seq_val}, accum={next_input}")
            computer.compute([seq_val, next_input])
            next_input = computer.outputs[-1]
        max_val = max(max_val, computer.outputs[-1])

    print(f"MAX: {max_val}")


def part2():
    all_outputs = set()
    computers = []
    input_queues = []
    threads = []
    phase_sequences = list(permutations(range(5, 10)))
    # phase_sequences = [(9,8,7,6,5)]
    program_override = None # [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    for phase_sequence in phase_sequences:
        for i in range(5):
            computers.append(IntCodeComputer(program_override or day7_parsed, id=f"amp{i}"))
            input_queues.append(queue.Queue())
            print(f"{i}: {input_queues[i]}")

        for i in range(5):
            comp_thread = threading.Thread(
                target=computers[i].compute,
                args=(input_queues[i], input_queues[i + 1 if i <= 3 else 0])
            )
            threads.append(comp_thread)

        for i in range(4, -1, -1):
            threads[i].start()
            input_queues[i].put(phase_sequence[i])

        input_queues[0].put(0)

        for i in range(5):
            threads[i].join()

        final_output = computers[4].outputs[-1]

        # reset everything in case we are still iterating
        threads.clear()
        input_queues.clear()
        computers.clear()

        print(f"final_output: {final_output}")
        all_outputs.add(final_output)

    print(f"overall max: {max(all_outputs)}")


if __name__ == "__main__":
    part2()

