import itertools
from collections import defaultdict
from typing import List

from attr import dataclass

""" input for this one is just:
Player 1 starting position: 3
Player 2 starting position: 7
"""

# there's almost certainly a non-iterative way to solve this, but I'm assuming
# part 2 will be not a random die...

DEBUG = False


def roll(die_range):
    yield from itertools.cycle(die_range)


if __name__ == "__main__":
    board = [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # part 1:
    position = [3, 7]
    score = [0, 0]
    rolls = roll(range(1, 101))
    turn = 0

    while True:
        player = turn % 2
        turn += 1
        die = [next(rolls), next(rolls), next(rolls)]
        move = sum(die)

        position[player] = board[(position[player] + move) % 10]
        score[player] += position[player]
        if score[player] >= 1000:
            # player is winner
            loser = (player + 1) % 2
            print(f"part 1: {score[loser] * (3 * turn)}")
            break

    # part 2:
    # for a first naive approach will just try to (mostly) brute force iteratively.
    # Presumably the problem is designed to make this not feasible but if it will work, I'm playing catch-up already..
    # as in part 1, track position and score, but now do so on a per-universe basis
    # to make this easier to reason over, create an actual Universe class that encapsulates position and score
#    @dataclass(eq=True, frozen=True)
    class Universe:
        position: List[int]
        score: List[int]
        instance_count: int = 0

        def __init__(self, starting_pos, starting_score):
            self.position = starting_pos
            self.score = starting_score

        def winner(self):
            if self.score[0] >= 21:
                return 1  # use actual "player numbers" so we can lean on falsey-ness of None
            elif self.score[1] >= 21:
                return 2
            else:
                return None

    """ in each universe, each turn will spawn 27 (3^3) new universes with rolls of:
        1, 1, 1
        1, 1, 2
        1, 1, 3
        1, 2, 1
        1, 2, 2
        [...]
        3, 2, 3
        3, 3, 1
        3, 3, 2
        3, 3, 3
    creating a distribution of moves that range between 3 and 9
    we don't actually need to consider the individual rolls, just the moves..
    """
    # could just compute this but I don't feel like fussing with getting the equation exactly right so I'll just gen it:
    moves_per_turn = defaultdict(lambda: 0)
    die = [None, None, None]
    for i in range(1, 4):
        die[0] = i
        for j in range(1, 4):
            die[1] = j
            for k in range(1, 4):
                die[2] = k
                moves_per_turn[sum(die)] += 1
    # there is also a finite (large, but finite) state of possible universe states so we don't really need to simulate
    # each one individually
    universes_by_state = defaultdict(lambda: 0)
    #universes_in_progress = {Universe([3, 7], [0, 0]), Universe([3, 7], [0, 0])}
    if DEBUG:
        universes_by_state[((4, 8), (0, 0))] = 1
    else:
        universes_by_state[((3, 7), (0, 0))] = 1
    winners = [0, 0]
    while len(universes_by_state) > 0:
        print(len(universes_by_state), sum(universes_by_state.values()))
        player = turn % 2
        turn += 1

        for state, state_count in list(universes_by_state.items()):  # iterate over a static list since we'll change this during loop
            # moving (starting) current entries out of this state so it will now be zero
            universes_by_state[state] -= state_count

            for move, move_count in moves_per_turn.items():
                position = list(state[0])
                score = list(state[1])
                position[player] = board[(position[player] + move) % 10]
                score[player] += position[player]
                val = state_count * move_count
                universes_by_state[(tuple(position), tuple(score))] += val

        for state, state_count in list(universes_by_state.items()):
            if state_count == 0:
                del universes_by_state[state]
            for i in (0, 1):
                if state[1][i] >= 21:
                    winners[i] += state_count
                    del universes_by_state[state]

    print(f"part 2: {max(winners)} from {winners}")
    if DEBUG:
        print(f"expected: 444356092776315; diff = {max(winners) - 444356092776315}")
    pass








