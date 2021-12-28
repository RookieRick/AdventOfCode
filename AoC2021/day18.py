import tqdm
import typing

from enum import IntEnum
from math import floor, ceil
from util.base_processor import DailyProcessorBase
from util import input_parser

SPLIT_DEPTH = 4


class Node:
    class NodeType(IntEnum):
        PAIR = 1
        TUPLE = 2
        INT = 3

    def __init__(self, node_type: NodeType = None, value=None):
        self.node_type = node_type
        self._parent: Node = None
        self._children: typing.List[Node] = [None, None]
        self._depth = 0
        self.value = value

    def __repr__(self):
        return f"{str(self.node_type)}: {self.value}"

    @property
    def depth(self) -> int:
        return self._depth

    @depth.setter
    def depth(self, val):
        self._depth = val
        if self._children[0] is not None:
            self._children[0].depth = val + 1
        if self._children[1] is not None:
            self._children[1].depth = val + 1

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        self._parent = val
        if self._parent is not None:
            self.depth = self._parent.depth + 1

    @property
    def left(self):
        return self._children[0]

    @left.setter
    def left(self, val):
        self._children[0] = val
        if self._children[0] is not None:
            self._children[0].parent = self  # this will propagate depth updates as well

    @property
    def right(self):
        return self._children[1]

    @right.setter
    def right(self, val):
        self._children[1] = val
        if self._children[1] is not None:
            self._children[1].parent = self  # this will propagate depth updates as well

    def traverse(self):
        if self.left is not None:
            yield from self.left.traverse()
        yield self
        if self.right is not None:
            yield from self.right.traverse()

    def reduce(self):
        # room to optimize here, especially if it turns out that in part 2 starting over and reprocessing the whole
        # tree every time is too costly... but for now, just reprocess the whole tree when anything changes
        # that includes things like split (originally I thought to collect a list of splittable nums while processing
        # explodes and then running through them sequentially (until one introduced a new explode candidate)
        # but that gets complicated when you have a tuple with both values getting split.. e.g., splits list contains
        # (node, 0) and (node, 1) - but once you process node, 0 split, when you try to process node, 1 split, node
        # no longer points to the right thing.
        reduce_completed = False
        while not reduce_completed:
            # first stage: explode deeply nested tuples
            last_int: typing.Tuple[Node, typing.Any] = None  # if we find a deeply nested tuple, we'll need the last int node encountered
            exploding_node: Node  = None
            next_int: typing.Tuple[Node, typing.Any] = None
            splits = []  # we can pre-collect these while looking for explode candidates
            for node in self.traverse():
                if exploding_node is None and node.node_type == Node.NodeType.INT:
                    last_int = (node, None)
                    if node.value >= 10:
                        splits.append((node, None))  # By the time we are done with explodings we'll eventually traverse entire tree in this loop
                elif exploding_node is None and node.node_type == Node.NodeType.TUPLE:
                    if node.depth >= SPLIT_DEPTH:
                        exploding_node = node
                    else:
                        last_int = (node, 1)
                        for i in (0, 1):
                            if node.value[i] >= 10:
                                splits.append((node, i))
                elif exploding_node is not None and node.node_type == Node.NodeType.INT:
                    next_int = (node, None)
                    break
                elif exploding_node is not None and node.node_type == Node.NodeType.TUPLE:
                    next_int = (node, 0)
                    break

            if exploding_node:
                # we found a node to explode:
                if last_int is not None:
                    if last_int[0].node_type == Node.NodeType.INT:
                        last_int[0].value += exploding_node.value[0]
                    else:  # TUPLE
                        vals = list(last_int[0].value)  # we COULD just store this as lists at this point but having them naturally print as (a, b) is helpful in debugging lololol
                        vals[last_int[1]] += exploding_node.value[0]
                        last_int[0].value = tuple(vals)
                if next_int is not None:
                    if next_int[0].node_type == Node.NodeType.INT:
                        next_int[0].value += exploding_node.value[1]
                    else:  # TUPLE
                        vals = list(next_int[0].value)
                        vals[next_int[1]] += exploding_node.value[1]
                        next_int[0].value = tuple(vals)

                exploding_node.node_type = Node.NodeType.INT
                exploding_node.value = 0
                # see if we just created a new tuple:
                parent = exploding_node.parent
                if (
                        parent and parent.node_type == Node.NodeType.PAIR and
                        parent.right.node_type == Node.NodeType.INT and parent.left.node_type == Node.NodeType.INT
                ):
                    parent.node_type = Node.NodeType.TUPLE
                    parent.value = (parent.left.value, parent.right.value)
                    parent.left = None
                    parent.right = None
            else:  # nothing left to explode, proceed with splits
                if len(splits) == 0:
                    reduce_completed = True
                else:
#                    while len(splits) > 0:
                        split = splits.pop(0)
                        # split may be an INT node (which can just become a tuple)
                        # OR a tuple node (in which case we need to figure out which of the values >= 10)
                        if split[0].node_type == Node.NodeType.INT:
                            split[0].node_type = Node.NodeType.TUPLE
                            halved = split[0].value / 2
                            split[0].value = (floor(halved), ceil(halved))
                        else:  # TUPLE
                            # TUPLE nodes are leaf nodes, so no need to worry about any children.
                            # we will just grow the tree downward here and create a new PAIR,
                            # splitting the value(s) in the tuple as needed
                            split[0].node_type = Node.NodeType.PAIR
                            for i in (0, 1):
                                if i == split[1]:
                                    child = Node(Node.NodeType.TUPLE)
                                    halved = split[0].value[i] / 2
                                    child.value = (floor(halved), ceil(halved))
                                else:
                                    child = Node(Node.NodeType.INT, split[0].value[i])
                                if i == 0:
                                    split[0].left = child
                                else:
                                    split[0].right = child
                            split[0].value = None
                        # if split[0].depth + 1 >= SPLIT_DEPTH:
                        #     # we've introduced a new tuple node with deep enough nesting to trigger an explode
                        #     # so break out here and let the outer loop keep on loopin'
                        #     break

    def magnitude(self):
        if self.node_type == Node.NodeType.INT:
            return self.value
        elif self.node_type == Node.NodeType.PAIR:
            left_mult = 3 * self.left.magnitude() if self.left is not None else 0
            right_mult = 2 * self.right.magnitude() if self.right is not None else 0
            return left_mult + right_mult
        else:  # implicit: TUPLE
            return 3 * self.value[0] + 2 * self.value[1]

    def serialize(self):
        if self.node_type == Node.NodeType.PAIR:
            return f"[{self.left.serialize()}, {self.right.serialize()}]"
        else:
            return f"{self.value}"


def build_subtree(input_data, parent=None):
    # input_data should always be a 2-element list
    # if parent is None, construct a ROOT Node, else a PAIR node
    # recursively set left/right to parse_subtree on each half in input_data
    # Note we'll have to be careful not to break apart any 2 entry lists of ints as those are
    # considered "numbers"
    if type(input_data) is int:
        node = Node(Node.NodeType.INT, input_data)
    else:  # must be a list
        assert len(input_data) == 2, "Unexpected input shape, should be a 2-element list"

        if type(input_data[0]) == type(input_data[1]) == int:
            node = Node(Node.NodeType.TUPLE, tuple(input_data))
        else:
            node = Node(Node.NodeType.PAIR)
            node.left = build_subtree(input_data[0], node)
            node.right = build_subtree(input_data[1], node)

    return node


class Day18Processor(DailyProcessorBase):
    def __init__(self, debug=False):
        super().__init__(18, debug=debug)

    def process(self):
        super().process()  # load data

        fish_trees = [build_subtree(data) for data in self.data]
        added = None
        for tree in tqdm.tqdm(fish_trees):
            if added is None:
                added = tree
            else:
                # "add" the trees by merging them
                root = Node(Node.NodeType.PAIR)
                root.left = added
                root.right = tree
                added = root
                # self.print_debug("added:")
                # self.print_debug(added.serialize)
                added.reduce()
                self.print_debug("added + reduced:")
                self.print_debug(added.serialize)

        result = added.magnitude()
        print(f"part 1: {result}")
        pass

        # presumably order matters with addition here so calc entire NxN matrix of magnitudes (except n=n diagonal)
        # (unless that proves too inefficient, but results for part 1 were plenty fast so fingers crossed.. ;) )
        # we only care about the largest possible mag so we don't actually need to store all the results
        # also need to re-read our input file here because during part 1 we'll have mangled individual trees
        super().process()  # filthy way to reload data, but this is hobby code and I'm tired of working on this one

        max_mag = 0
        # unlike part 1, leave these as lists loaded from JSON, create temporary working copies of trees
        # each iteration because the act of adding and reducing mangles the trees
        for tree1 in tqdm.tqdm(self.data):
            for tree2 in self.data:
                if tree1 == tree2:
                    pass  # don't add self
                else:
                    # "add" the 2 subtrees
                    root = Node(Node.NodeType.PAIR)
                    root.left = build_subtree(tree1, root)
                    root.right = build_subtree(tree2, root)
                    root.reduce()
                    max_mag = max(max_mag, root.magnitude())
        print(f"part 2: {max_mag}")


if __name__ == "__main__":
    processor = Day18Processor(debug=False)
    processor.input_transforms = [input_parser.JsonLoad()]
    processor.process()
