from typing import List
from contextlib import suppress
import tqdm

from util import input_parser
from util.base_processor import DailyProcessorBase


AXES = {"x": 0, "y": 1, "z": 2}

DEBUG = False  # "global" debug for when we wanna print stuff regardless of whether actually in "debug" mode
DEBUG_INDENT = [0]


class Cuboid:
    # ranges is a 3-element list, corresponding to x, y, z dimensions.
    # value for each of those is a range object
    ranges: List
    state: int   # 0 for off, 1 for on
    on_cells: int  # number of cells in this Cuboid that contribute to FINAL "on" state
    intersections: List
    parent_manifold: set

    def __init__(self, input_ranges, state=0, parent_manifold=None):
        self.parent_manifold = parent_manifold
        self.state = state
        self.intersections = []
        if isinstance(input_ranges, list):
            self.ranges = input_ranges.copy()
        else:
            self.ranges = [None, None, None]
            dimensions = input_ranges.split(",")
            for i in (0, 1, 2):
                axis, axis_range = dimensions[i].split("=", maxsplit=1)
                axis = AXES[axis]
                range_ends = [int(val) for val in axis_range.split("..", maxsplit=1)]
                self.ranges[axis] = range(range_ends[0], range_ends[1] + 1)

            if self.state == 1:
                self.on_cells = self.magnitude()
            else:
                self.on_cells = 0

    def __repr__(self):
        return ','.join([f"{list(AXES.keys())[i]}={self.ranges[i]}" for i in range(3)]) + (" [ON]" if self.state else " [OFF]")

    def __hash__(self):
        return hash(tuple(self.ranges))

    def __eq__(self, other):
        return self.ranges == other.ranges

    def __sub__(self, other):
        # "subtract" another cube from this one by slicing this one into pieces and discarding the pieces that match
        # subtract assumes "other" is contained in this cube (i.e., it was the result of an intersection operation)
        if DEBUG:
            print(f"{'.' * DEBUG_INDENT[0]}subtracting: {self} - {other}")
        if other == self:
            # obliterate
            return {}
        intersection = self.intersect(other)
        if intersection is None:
            # no overlap, return unmodified
            return self

        # there is overlap. Slice this cube into sub-cubes until we can remove the overlap
        pieces = set()
        keep = set()

        potential_ranges = [axis_spec for axis_spec in enumerate(other.ranges) if axis_spec[1] != self.ranges[axis_spec[0]]]
        # maybe arbitrary but instinctively seems like might leave us fewer, larger cuboids..
        # so we'll split on the shortest axis of intersection first:
        potential_ranges.sort(key=lambda x: len(x[1]))  # sort by magnitude
        axis = potential_ranges[0][0]
        cutpoint = -1 * len(potential_ranges[0][1])
        split_axes = [self.ranges.copy(), self.ranges.copy()]

        split_axes[0][axis] = split_axes[0][axis][:cutpoint]
        split_axes[1][axis] = split_axes[1][axis][cutpoint:]
        pieces.add(Cuboid(split_axes[0], self.state, self.parent_manifold))
        pieces.add(Cuboid(split_axes[1], self.state, self.parent_manifold))

        while pieces:
            if DEBUG:
                print(f"{'.' * DEBUG_INDENT[0]}sub-processing {len(pieces)} pieces: {pieces}")
            cascading_subtractions = set()
            for piece in pieces.copy():  # grab a copy to iterate over since we'll mod the set during loop
                sub_intersection = self.intersect(piece)
                pieces.remove(piece)
                if not sub_intersection:
                    keep.add(piece)
                else:
                    DEBUG_INDENT[0] += 1
                    pieces.update(piece - sub_intersection)
                    DEBUG_INDENT[0] -= 1

        return keep

    def magnitude(self):
        mag = 1
        for axis_range in self.ranges:
            mag *= len(axis_range)
        return mag

    def contains(self, x, y, z):
        return x in self.ranges[0] and y in self.ranges[1] and z in self.ranges[2]

    def intersect(self, other):
        # find intersection (if any) between this and another cuboid:
        try:
            ranges = [
                range(max(self.ranges[i][0], other.ranges[i][0]), min(self.ranges[i][-1], other.ranges[i][-1]) + 1) or None
                for i in range(3)
            ]
        except IndexError:
            # 0-length range like (4, 4) can't be indexed (and indicates that we are adjacent, not intersecting)
            ranges = [None, None, None]
        return Cuboid(ranges) if all(ranges) else None


class Day22Processor(DailyProcessorBase):
    def __init__(self):
        super().__init__(
            day=22,
            input_transforms=[input_parser.Split("\\s")],
            debug=True
        )

    def process(self):
        super().process()  # load data
        cuboids = [Cuboid(data[1], 1 if data[0] == "on" else 0) for data in self.data]

        # # part 1 - simple dumb iterative approach that obvs is not going to work for part 2... ;)
        # # the last cuboid to touch a given point will determine that point's state
        # cuboids.reverse()
        #
        # on = 0
        # off = 0
        # for x in tqdm.tqdm(range(-50, 51)):
        #     for y in range(-50, 51):
        #         for z in range(-50, 51):
        #             # only the last cuboid to affect a point will matter:
        #             for cuboid in cuboids:
        #                 if cuboid.contains(x, y, z):
        #                     if cuboid.state:
        #                         on += 1
        #                     else:
        #                         off += 1
        #                     break
        #
        # print(f"part 1: {on}")

        # part 2. We can't iterate over this massive space..  Operate on the cuboids themselves:
        # we'll build a (not necessarily connected) "manifold" of "on" cuboids and carve them up as needed
        # once we've processed all the cuboids then we can just add the magnitudes of what remains.
        on_manifold = set()

        def process_cuboid(cuboid):
            if DEBUG:
                print(f"{'.'*DEBUG_INDENT[0]}process_cuboid({cuboid}) vs {len(on_manifold)} manifold cubes")
            intersections = {on_cube: cuboid.intersect(on_cube) for on_cube in on_manifold}
            intersections = {k: v for k, v in intersections.items() if v is not None}
            if not intersections:
                # no intersection. If this one is "on" just add to manifold.
                # if it's "off" then it has no effect so just ignore it.
                if cuboid.state == 1:
                    if DEBUG:
                        print(f"{'!'*DEBUG_INDENT[0]}add to manifold: {cuboid}")
                    on_manifold.add(cuboid)
                    return
            else:
                # this cube intersects with one or more cubes in the manifold, split based on first one and
                # recurse through remaining cubes
                # (we only use the first one because we'll split ourselves based on that and then reprocess all of
                # the "child" cubes we spawned - those will get re-evaluated vs the whole manifold until we eventually
                # reduce to a set of cubes that don't intersect with ANY in the manifold
                intersection = list(intersections.values())[0]
                if cuboid.state == 1:
                    pieces = {cuboid}
                    # cube is "on", slice it to remove the portions that intersect and add remainder to manifold
                    while pieces:
                        piece = pieces.pop()
                        sub_pieces = piece - intersection
                        DEBUG_INDENT[0] += 1
                        for sub_piece in sub_pieces:
                            process_cuboid(sub_piece)
                        DEBUG_INDENT[0] -= 1
                else:
                    # cube is "off", slice the manifold cube(s) with which it intersects and discard those portions
                    for on_cube, intersection in intersections.items():
                        on_manifold.remove(on_cube)
                        on_manifold.update(on_cube - intersection)

        for cuboid in tqdm.tqdm(cuboids):
            if DEBUG_INDENT[0] != 0:
                print(f"***** WTF {DEBUG_INDENT}")
            else:
                print("=" * 50)
                print(f"TOP LEVEL PROCESS: {cuboid}")
                print("=" * 50)
            process_cuboid(cuboid)

        # our "on" manifold should now be constructed.
        # part 1:
        region_of_interest = Cuboid([range(-50, 51), range(-50, 51), range(-50, 51)])
        intersections = filter(None, [region_of_interest.intersect(on_cube) for on_cube in on_manifold])
        print(f"part 1: {sum([intersection.magnitude() for intersection in intersections])}")

        self.print_debug(f"on_manifold mag={sum([on_cube.magnitude() for on_cube in on_manifold])}")
        pass


if __name__ == "__main__":
    processor = Day22Processor()
    processor.process()
