from AdventOfCode.AoC2019.inputs import get_input
from AdventOfCode.AoC2019.intcode import IntCodeComputer


data = get_input(9)

#data = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
computer = IntCodeComputer(data)
computer.compute()
