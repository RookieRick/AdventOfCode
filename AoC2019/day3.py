from AdventOfCode.AoC2019.inputs import day3_parsed


class Point2D(object):
    x = 0
    y = 0

    def __init__(self, x_in, y_in):
        self.x = x_in
        self.y = y_in

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

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


def parse_move(descriptor):
    direction = descriptor[:1]
    magnitude = int(descriptor[1:])
    delta = Point2D(0, 0)
    if direction == 'R':
        delta.x = magnitude
    elif direction == 'L':
        delta.x = -magnitude
    elif direction == 'U':
        delta.y = magnitude
    elif direction == 'D':
        delta.y = -magnitude
    return delta


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


def main():
    wire_segments = [[], []]

    for i in range(2):
        current_point = Point2D(0, 0)
        cumulative_length = 0
        for move in day3_parsed[i][:50]:  # we likely don't need to examine the whole length for part 2.. just a guess for now ;)
            delta = parse_move(move)
            next_point = current_point + delta
            wire_segments[i].append((Vector2D(current_point, next_point), cumulative_length))
            # recorded length at START of vector, now set up for next vector:
            cumulative_length += abs(delta.x) + abs(delta.y)
            current_point = next_point

    all_intersections = set()

    total = len(wire_segments[0]) * len(wire_segments[1])
    print(f"total segs={total}")
    counter = 0
    for v1_with_steps in wire_segments[0]:
        for v2_with_steps in wire_segments[1]:
            counter += 1
            if counter % 100 == 0:
                print(f"{counter}")
            all_intersections.update(get_intersections_with_length(v1_with_steps, v2_with_steps))
    print(f"wire 1: {wire_segments[0]}")
    print(f"wire 2: {wire_segments[1]}")
    print(f"intersections:{all_intersections}")

    print(f"wire 1 seg 1 points{wire_segments[0][0][0].to_points_with_steps(wire_segments[0][0][1])}")
    print(f"wire 1 seg 2 points{wire_segments[0][1][0].to_points_with_steps(wire_segments[0][1][1])}")
    print(f"wire 2 seg 1 points{wire_segments[1][0][0].to_points_with_steps(wire_segments[1][0][1])}")
    print(f"wire 2 seg 2 points{wire_segments[1][1][0].to_points_with_steps(wire_segments[1][1][1])}")

    all_intersections.remove((Point2D(0,0), 0))

    #part 1:
    #and since we're measuring from origin.. don't need vectors, just points:
    distances = (abs(point.x) + abs(point.y) for (point, distance) in all_intersections)
    print(f"min dist (taxicab)={min(distances)}")
    #part 2:
    distances = (distance for (point, distance) in all_intersections)
    print(f"min dist (steps)={min(distances)}")



if __name__ == "__main__":
    main()
