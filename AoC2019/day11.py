from AoC2019.inputs import get_input
from AoC2019.intcode import IntCodeComputer
from collections import defaultdict
import queue
import math
# initial thoughts..
# build a hash of (x, y) -> color [default black = 0] to represent hull.
# don't really care where the robot starts..
# assume x, y standard cartesian coords..

HALF_PI = math.pi / 2
TWO_PI = math.pi * 2

DEBUG = False


class Robot(object):
    def __init__(self, computer, hull_paint):
        self.current_x = 0
        self.current_y = 0
        self.computer = computer
        self.hull_paint = hull_paint
        self.input_queue = queue.Queue()
        self.cells_painted = set()
        self.orientation = 0  # define zero as "north"

        # additional registers for tracking extents visited
        self.min_x = self.min_y = self.max_x = self.max_y = 0

    def move_and_read_hull_color(self):
        if not self.input_queue.empty(): # we have a move to do..
            # assumption - outputs get added in pairs per instructions
            # computer will generate 2 outputs BEFORE calling for next input..
            paint_color = int(self.input_queue.get())
            turn_instr = int(self.input_queue.get())
            self.paint(self.current_x, self.current_y, paint_color)
            # for turn:  0 = turn left, 1 = turn right
            turn_dir = -1 if turn_instr == 0 else 1
            self.orientation = self.orientation + turn_dir * HALF_PI
            if math.fabs(self.orientation) == TWO_PI:
                self.orientation = 0
            # be wary, trig functions don't actually eval to 0 at e.g. math.pi / 2, but we can just round to nearest int
            delta_x = round(math.sin(self.orientation))
            delta_y = round(math.cos(self.orientation))

            self.current_x += delta_x
            self.current_y += delta_y
            if DEBUG:
                print(f"{math.degrees(self.orientation)} --> ({delta_x}, {delta_y}) --> ({self.current_x}, {self.current_y})")

            self.min_x = min(self.min_x, self.current_x)
            self.min_y = min(self.min_y, self.current_y)
            self.max_x = max(self.max_x, self.current_x)
            self.max_y = max(self.max_y, self.current_y)

        return self.hull_paint[(self.current_x, self.current_y)]

    def paint(self, x, y, color):
        coord = (x, y)
        self.hull_paint[coord] = color
        self.cells_painted.add(coord)

    def run(self):
        # just do this synchronously for now..
        self.computer.compute(self.move_and_read_hull_color, self.input_queue)



def main():
    program = get_input(11)

    computer = IntCodeComputer(program)
    hull_paint = defaultdict(lambda: 0)  # intended key is (x, y) tuple cartesian coords
    # part two: start on a white cell:
    hull_paint[(0, 0)] = 1
    robot = Robot(computer, hull_paint)
    robot.run()

    print(f"# of unique cells painted: {len(robot.cells_painted)}")

    # to render what was actually painted..
    # find extents of cells visited..  actually we can build tracking of that into our robot for convenience
    print(f"extents: {robot.min_x}, {robot.min_y} to {robot.max_x}, {robot.max_y}")
    print("--------------")
    # render "upside-down"
    SPLATS=[' ', '#']
    for y in range(robot.max_y, robot.min_y - 1, -1):
        scanline = ''.join([SPLATS[hull_paint[(x, y)]] for x in range(robot.min_x, robot.max_x + 1)])

        print(f"{scanline}   {y}")


if __name__ == "__main__":
    main()



