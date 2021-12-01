import AdventOfCode.util.input_parser as parser


DIRECTIONS = ['E', 'S', 'W', 'N']

class Point2D(object):
    x = 0
    y = 0

    def __init__(self, x_in, y_in):
        self.x = x_in
        self.y = y_in

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Point2D(self.x * other, self.y * other)

    def __str__(self):
        return f"{self.x},{self.y}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(str(self))


class Vector2D(object):
    start = Point2D(0,0)
    end = Point2D(0,0)

    def __init__(self, start_in, end_in):
        self.start = start_in
        self.end = end_in

    def __str__(self):
        return f"{self.start}-->{self.end}"

    def __repr__(self):
        return str(self)

    def to_points(self):
        # gonna go ahead and assume we don't have any "0" length moves..
        points = []
        direction_x = 1 if self.end.x > self.start.x else -1
        direction_y = 1 if self.end.y > self.start.y else -1

        for x in range(self.start.x, self.end.x + direction_x, direction_x):
            for y in range(self.start.y, self.end.y + direction_y, direction_y):
                points.append(Point2D(x, y))
        return points

    def to_points_with_steps(self, start_length):
        points_with_steps = []
        next_length = start_length
        for point in self.to_points():
            points_with_steps.append((point, next_length))
            next_length += 1
        return points_with_steps


def parse_move(descriptor, part=1, current_direction=None, waypoint=None):
    # assumes rotations are always 90 degrees..  if that changes, none of this will work and I'll regret
    # repurposing last year's day 3 code :P
    orientation = current_direction
    direction = descriptor[:1]
    magnitude = int(descriptor[1:])
    delta = Point2D(0, 0)

    if part == 1:
        if direction == 'F':
            direction = DIRECTIONS[orientation]

        if direction == 'E':
            delta.x = magnitude
        elif direction == 'W':
            delta.x = -magnitude
        elif direction == 'N':
            delta.y = magnitude
        elif direction == 'S':
            delta.y = -magnitude
        elif direction == 'R':
            orientation = (orientation + (int(magnitude/90))) % 4
        elif direction == 'L':
            orientation = (orientation - (int(magnitude/90))) % 4
    else:  # part 2
        if direction == 'F':
            delta = waypoint * magnitude
        elif direction == 'E':
            waypoint.x += magnitude
        elif direction == 'W':
            waypoint.x = -magnitude
        elif direction == 'N':
            waypoint.y = magnitude
        elif direction == 'S':
            waypoint.y = -magnitude
        elif direction == 'R' or direction == 'L':
            rotation = int(magnitude/90) * -1 if direction == 'L' else 1
            # TODO decompose it into 1-3 right turns (ignore 0).. then it's a simple nested if here..
            # something somethign rotation something


    return delta, orientation, waypoint



def get_intersections(vector1, vector2):
    # brutest of forces..
    return vector1.to_points().intersection(vector2.to_points())


def get_intersections_with_length(v1_with_steps, v2_with_steps):
    all_intersections = set()

    v1_points_with_steps = v1_with_steps[0].to_points_with_steps(v1_with_steps[1])
    v2_points_with_steps = v2_with_steps[0].to_points_with_steps(v2_with_steps[1])
    for (p1, p1_steps) in v1_points_with_steps:
        for (p2, p2_steps) in v2_points_with_steps:
            if p1 == p2:
                all_intersections.add((p1, p1_steps + p2_steps))
    return all_intersections


DEBUG = False


def main():
    filename = f"./raw_inputs/day12{'_debug' if DEBUG else ''}.txt"
    moves = parser.parse(filename)

    points = []

    current_point = Point2D(0, 0)
    waypoint = Point2D(10, 1)
    direction = 0  # we'll use 0 = east, 1 S, 2 W, 3 N..

    for part in (1, 2):
        for move in moves:
            delta, direction, waypoint = parse_move(move, part=part, current_direction=direction, waypoint=waypoint)
            current_point += delta



    # part 1 - manhattan distance
    print(f"{abs(current_point.x) + abs(current_point.y)}")

    print("fin.")


if __name__ == "__main__":
    main()
