import itertools
import queue

# hacky opcodes constants
ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
RELATIVE_BASE_ADJUST = 9
BREAK = 99

# even hackier debug const - could use logging with actual levels but... eeeeeeeh. I do need to do other life things
DEBUG = False

class Operation:
    num_inputs = 0
    includes_write = False

    def __init__(self, num_inputs, includes_write=False):
        """
        Assumes output is always last param
        :param num_inputs:
        :param includes_output:
        """
        self.num_inputs = num_inputs
        self.includes_write = includes_write


OPERATIONS = {
    ADD: Operation(3, True),
    MULTIPLY: Operation(3, True),
    INPUT: Operation(1, True),
    OUTPUT: Operation(1),
    JUMP_IF_TRUE: Operation(2),
    JUMP_IF_FALSE: Operation(2),
    LESS_THAN: Operation(3, True),
    EQUALS: Operation(3, True),
    RELATIVE_BASE_ADJUST: Operation(1),
    BREAK: Operation(0),
}


class IntCodeComputer(object):
    def __init__(self, program, id="COMPUTER"):
        """
        Initializes an IntCode computer
        :param program: the program (series of ints) to load
        :param id: optional computer ID
        """
        self.program = program
        self.inputs = []
        self.outputs = []
        self.id = id
        self.relative_base = 0

    def get_input(self):
        if type(self.inputs) is list and len(self.inputs) > 0:
            auto_input = self.inputs[0]
            self.inputs = self.inputs[1:]
            print(f"using input {auto_input}")
            return int(auto_input)
        elif type(self.inputs) is queue.Queue:
            queued_input = None
            while queued_input is None:
                queued_input = int(self.inputs.get())  # assumes threaded if using a queue..
            if DEBUG:
                print(f"pulled from queue {queued_input}")
            return int(queued_input)
        elif callable(self.inputs):
            return int(self.inputs())
        else:
            print("input:")
            return int(input())

    def compute(self, inputs=[], output_queue=None):
        """
        Start the computer, with optional overrides for default i/o
        :param inputs:  if a list, will consume inputs from list before switching to interactive.
                        if a queue, will read from queue (or block) when input is needed
                        if a callable, will invoke to get next input when needed
        :param output_queue:
        :return:
        """
        self.inputs = inputs
        working_copy = list(self.program)
        working_copy.extend([0] * 1000000) # lazy but effective..
        pos = 0
        self.relative_base = 0

        print(f"starting compute loop for {self.id} with input {self.inputs} output_queue={output_queue}")
        while True:
            instr = self.get_instr(working_copy, pos)
            opcode = instr[0]
            if DEBUG:
                print(f"{self.id}: {opcode}")
            args = instr[1:]

            next_pos = pos + len(instr)
            if opcode == BREAK:
                break
            elif opcode == ADD:
                working_copy[args[2]] = args[0] + args[1]
            elif opcode == MULTIPLY:
                working_copy[args[2]] = args[0] * args[1]
            elif opcode == INPUT:
                working_copy[args[0]] = self.get_input()
            elif opcode == OUTPUT:
                print(f"{self.id}: {args[0]}")
                self.outputs.append(args[0])
                if output_queue is not None:
                    if DEBUG:
                        print(f"{self.id} publishing {args[0]} to {output_queue}")
                    output_queue.put(args[0])
            elif opcode == JUMP_IF_TRUE:
                if args[0]:
                    next_pos = args[1]
            elif opcode == JUMP_IF_FALSE:
                if not args[0]:
                    next_pos = args[1]
            elif opcode == LESS_THAN:
                if args[0] < args[1]:
                    working_copy[args[2]] = 1
                else:
                    working_copy[args[2]] = 0
            elif opcode == EQUALS:
                if args[0] == args[1]:
                    working_copy[args[2]] = 1
                else:
                    working_copy[args[2]] = 0
            elif opcode == RELATIVE_BASE_ADJUST:
                self.relative_base += args[0]

            pos = next_pos
        print(f"{self.id}.compute returning")
        return working_copy

    def get_instr(self, program, instr_index):
        instr_input = str(program[instr_index])
        opcode = int(instr_input[-2:])
        param_modes = list(instr_input[:-2])
        param_modes.reverse()

        operation = OPERATIONS[opcode]

        instr = [opcode]
        num_args = operation.num_inputs
        param_modes.extend([0] * (num_args - len(param_modes))) # pad if needed

        for p_offset in range(1, num_args+1):
            mode_val = int(param_modes[p_offset-1:p_offset][0]) if param_modes[p_offset-1:p_offset] else 0
            immed_mode = mode_val == 1 or (operation.includes_write and p_offset == num_args)
            relative_mode = mode_val == 2
            rel_offset = 0 if not relative_mode else self.relative_base
            if immed_mode:
                instr.append(program[instr_index + p_offset] + rel_offset)
            else:
                instr.append(program[program[instr_index + p_offset] + rel_offset])

        return instr


def main():
    # #Day 2-1:
    # inputs = [1,0,0,0,99]
    # print(compute(inputs))

    #
    # #Day 2-2:
    # raw_input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,13,19,2,9,19,23,1,23,6,27,1,13,27,31,1,31,10,35,1,9,35,39,1,39,9,43,2,6,43,47,1,47,5,51,2,10,51,55,1,6,55,59,2,13,59,63,2,13,63,67,1,6,67,71,1,71,5,75,2,75,6,79,1,5,79,83,1,83,6,87,2,10,87,91,1,9,91,95,1,6,95,99,1,99,6,103,2,103,9,107,2,107,10,111,1,5,111,115,1,115,6,119,2,6,119,123,1,10,123,127,1,127,5,131,1,131,2,135,1,135,5,0,99,2,0,14,0]
    # for noun in range(100):
    #     for verb in range(100):
    #         raw_input[1] = noun
    #         raw_input[2] = verb
    #         if noun == 2 and verb == 6:
    #             print("whoa hoss")
    #         result = compute(raw_input)
    #         if result[0] == 19690720:
    #             print(result)
    #             print(100 * noun + verb) # correct = 3376
    #             break

    #Day 5:
    inputs = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,72,20,224,1001,224,-1440,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1002,147,33,224,101,-3036,224,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1102,32,90,225,101,65,87,224,101,-85,224,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,1102,33,92,225,1102,20,52,225,1101,76,89,225,1,117,122,224,101,-78,224,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,1102,54,22,225,1102,5,24,225,102,50,84,224,101,-4600,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,1102,92,64,225,1101,42,83,224,101,-125,224,224,4,224,102,8,223,223,101,5,224,224,1,224,223,223,2,58,195,224,1001,224,-6840,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,1101,76,48,225,1001,92,65,224,1001,224,-154,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,226,224,1002,223,2,223,1005,224,329,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,344,1001,223,1,223,1107,226,226,224,1002,223,2,223,1006,224,359,1001,223,1,223,8,226,226,224,1002,223,2,223,1006,224,374,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,389,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,404,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,419,101,1,223,223,1008,226,677,224,1002,223,2,223,1006,224,434,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,449,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,107,677,677,224,102,2,223,223,1005,224,479,101,1,223,223,7,226,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,7,677,677,224,102,2,223,223,1006,224,509,101,1,223,223,107,226,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,539,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,554,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,569,101,1,223,223,8,677,226,224,102,2,223,223,1006,224,584,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,599,1001,223,1,223,1007,677,226,224,1002,223,2,223,1005,224,614,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,629,101,1,223,223,1108,677,677,224,1002,223,2,223,1005,224,644,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,659,101,1,223,223,107,226,226,224,102,2,223,223,1005,224,674,101,1,223,223,4,223,99,226]
    #inputs = [1002,4,3,4,33]
    inputs = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    computer = IntCodeComputer(inputs)
    debug = computer.compute()
    #print(debug)
    #
    # debug= computer.compute([1])
    # print(debug)
    # print("fin.")


if __name__ == "__main__":
    main()