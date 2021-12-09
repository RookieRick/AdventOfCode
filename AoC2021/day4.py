import AdventOfCode.util.input_parser as parser
from collections import defaultdict
from numpy import transpose


class BoardNumber:
    def __init__(self, value, card):
        self.value = int(value)
        self.card = card
        self.marked = False


class Card:
    def __init__(self, rows):
        # rows should be a list of 5 strings, each with 5 nums
        # we don't have any storage constraints here so we're going to
        # preload both "rows" and "cols" collections to make check for winning conditions super easy
        self.rows = [[BoardNumber(value, self) for value in row.split()] for row in rows]
        self.cols = transpose(self.rows)
        self.done = False

    def winner(self):
        check_rows = any([all([value.marked for value in row]) for row in self.rows])
        check_cols = any([all([value.marked for value in col]) for col in self.cols])
        return check_rows or check_cols

    def unmarked(self):
        unmarked = []
        for row in self.rows:
            unmarked += [cell for cell in row if not cell.marked]

        return unmarked


if __name__ == "__main__":
    data = parser.parse("./raw_inputs/day4.txt")

    draws = [int(value) for value in data[0].split(',')]

    cards = []

    for i in range(1, len(data), 6):
        # first row is blank line separator
        # followed by 5 rows of 5 vals
        cards.append(Card(data[i+1:i+6]))

    # num_lookup will allow us to avoid iterating over every card for every number called, just go straight to the
    # relevant board number:
    num_lookup = defaultdict(set)
    for card in cards:
        for row in card.rows:
            for cell in row:
                num_lookup[cell.value].add(cell)

    # part 1 (and 2, combined):
    for part in (1, 2):
        winner = None
        winning_number = None
        for draw in draws:
            for cell in [incomplete for incomplete in num_lookup[draw] if not incomplete.card.done]:
                cell.marked = True
                if cell.card.winner():
                    winner = cell.card
                    winning_number = draw  # not strictly needed but let's not rely on loop iterators after the loop
                    cell.card.done = True
                    if part == 1:  # find FIRST winner, otherwise keep going until we find LAST winner
                        break
            else:
                continue
            break

        if winner:
            unmarked_vals = sum([cell.value for cell in winner.unmarked()])
            print(f"winner: {unmarked_vals} * {winning_number} = {unmarked_vals * winning_number}")
        else:
            print("NO WINNER? WTF")


    print("fin.")