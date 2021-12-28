from util import input_parser
from util.base_processor import DailyProcessorBase


class Day6Processor(DailyProcessorBase):

    def __init__(self, debug=False):
        super().__init__(
            day=6,
            input_blob=True,
            input_transforms=[input_parser.Cast(int), input_parser.Split(',')],
            debug=debug
        )

    def process(self):
        super().process()  # load input

        """
        Short shameful confession. Even knowing better upon seeing the word "exponential" in the problem,
        I first tried an iterative approach (modeling every fish as an object) - which worked for part 1, and presumably
        would have worked for part 2 had I let it run for hours.
        I then spent a fair bit of time trying to think of a way to derive an equation to just solve mathematically
        ..and reminded myself in the process how long it's been since I've done any serious calculus ;)
        Played around briefly with a recursive solution (to approximate a mathematical) but that seems fraught with the
        same potential issues of scale.
        So now I've surrendered my dignity and went and read about how other people solved this and it's so 
        simple and elegant. I'll at least do my own implementation based on the concept for the sake of completeness
        and not crib anyone else's actual code... lol
        """

        # don't model fish. model "types" of fish where fish can be binned by "how many days until spawn"
        # and (despite my guess that we might for part 2), we never care about anything other than the count
        # of fish, so we don't need to maintain ANY info about the individual fishes:

        # simple array to bin fish by days to spawn.
        # initially configured as you would expect:  fish_by_timer[0] gives the number of fish with timer=0
        # Rather than have to constantly re-build the array though, as we iterate over time we'll just shift the "zero"
        # point and treat this like a circular array
        fish_by_timer = [0] * 9
        spawn_index = 0

        def get_index(i):
            return i % 9

        for val in self.data:
            fish_by_timer[val] += 1

        for day in range(256):
            # count how many fish are spawning this day:
            spawning_fish = fish_by_timer[get_index(spawn_index)]
            # now move our zero point.
            spawn_index = get_index(spawn_index + 1)
            # Note that this makes our OLD zero point the new
            # "9 days from now" so it's value accounts for the new fish that are being spawned.
            # so we can "move" the spawning fish to "7 days from now" by just adding them to the updated zero index
            fish_by_timer[get_index(spawn_index+6)] += spawning_fish

            if day == 79:
                print(f"part 1: {sum(fish_by_timer)}")

        print(f"part 2: {sum(fish_by_timer)}")


if __name__ == "__main__":
    processor = Day6Processor(debug=False)
    processor.process()

