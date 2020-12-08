import AdventOfCode.AoC2020.input_parser as parser
import re
from collections import defaultdict

PART = 2
DEBUG = False


def _debug(msg):
    if DEBUG:
        print(msg)


if __name__=="__main__":
    filename = f"./raw_inputs/day8{'_debug' if DEBUG else ''}.txt"
    instructions = parser.parse(filename, transforms=[parser.Split(' ')])
    for instruction in instructions:
        instruction[1] = int(instruction[1])

    accumulator = 0
    instr_ptr = 0
    visited = set()
    nop_jmp_switch = 0
    nop_jmp_counter = 0

    while True:
        if instr_ptr in visited:
            print(f"Loop detected. Accum = {accumulator}")
            if PART == 1:
                break
            elif PART == 2:
                instr_ptr = 0
                accumulator = 0
                nop_jmp_counter = 0
                nop_jmp_switch += 1
                visited = set()

        if instr_ptr >= len(instructions):
            print(f"Program terminated. Accum = {accumulator}")
            break

        _debug(f"{instr_ptr} {accumulator} {instructions[instr_ptr]}")

        visited.add(instr_ptr)
        op = instructions[instr_ptr][0]
        if op in ('jmp', 'nop'):
            _debug(f"{op} detected at {instr_ptr}")
            if nop_jmp_counter == nop_jmp_switch:
                op = 'jmp' if op == 'nop' else 'nop'
                _debug(f"Op changed to {op}")
            nop_jmp_counter += 1
        arg = instructions[instr_ptr][1]
        jmp = 1
        if op == 'acc':
            accumulator += arg
        elif op == 'jmp':
            jmp = arg
        elif op == 'nop':
            pass
        instr_ptr += jmp

    print("fin.")


