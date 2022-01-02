from util.base_processor import DailyProcessorBase
from util.input_parser import Split


class Decoder:
    def __init__(self, samples):
        self.decoder_ring = {}
        self.encoder_ring = {}  # redundant but easy to build and should make life easier when deducing..
        samples_by_len = {i: set() for i in range(2, 8)}
        for sample in [''.join(sorted(sample)) for sample in samples]: # sort the strings for easy comparisons later
            samples_by_len[len(sample)].add(sample)

        # the "easy ones": distinct values so will only have one entry in list of samples by len
        for length, value in [(2, 1), (3, 7), (4, 4), (7, 8)]:
            assert(len(samples_by_len[length]) == 1)
            sample = next(iter(samples_by_len[length]))
            self.decoder_ring[sample] = value
            self.encoder_ring[value] = set(sample)

        self.segments = [None] * 7
        # 2 segments: 1
        # 3 segments: 7
        # 4 segments: 4
        # 5 segments: 2, 3, 5,
        # 6 segments: 0, 6, 9
        # 7 segments: 8
        # we'll first build thes as sets to keep the "arithmetic" simple. When done, each should be a single-element set

        # "a": 1 and 7 share c, f, but not a. So we can determine 'a':
        self.segments[0] = self.encoder_ring[7] - self.encoder_ring[1]

        # "d": 5-segment digits 2, 3, 5 all include 'd' as does 4. Excluding c and f (we know that PAIR, not the singles), that's common denom
        self.segments[3] = self.encoder_ring[4].intersection(*samples_by_len[5]) - self.encoder_ring[1]

        # "g":  now since we can remove 'd' we can do same thing for 'g', the only fully-unknown in our 5-segment digits:
        # we can use 8 as the basis to find intersection of all 5-length samples since it's includes everything
        self.segments[6] = self.encoder_ring[8].intersection(*samples_by_len[5]) - set(self.segments[3]).union(self.segments[0])

        # "b": for 'b', we can now just subtract  'c''f'(aka 1) and already determined 'd' from 4:
        self.segments[1] = self.encoder_ring[4] - self.encoder_ring[1] - set(self.segments[3])

        # "f": now from 5 we can subtract 'a', 'b', 'd', and 'g' to find 'f':
        # we have to deduce which is 5 though. it's one of the 3 5-segment digits.. and should be the only one
        # that has one unknown after subtracting all the knowns
        knowns = set.union(*[segment for segment in self.segments if segment is not None])
        subtracted = [set(sample).difference(knowns) for sample in samples_by_len[5]]
        subtracted = [element for element in subtracted if len(element) == 1]  # filter down to "5"
        assert(len(subtracted) == 1)
        self.segments[5] = subtracted[0]

        # "c" we're getting down to the easy bits now. 'c' is the unknown half of 1:
        self.segments[2] = self.encoder_ring[1] - self.segments[5]

        # "e" - all that's left:
        self.segments[4] = set("abcdefg").difference(set.union(*[segment for segment in self.segments if segment]))

        # final sanity check:
        assert(set.union(*self.segments) == set("abcdefg"))

        # and lastly unroll our sets back into single chars:
        self.segments = [segment.pop() for segment in self.segments]

        # and finish making our "rings":
        for segment_indices, value in [
            ([0, 1, 2, 4, 5, 6], 0),
            ([0, 2, 3, 4, 6], 2),
            ([0, 2, 3, 5, 6], 3),
            ([0, 1, 3, 5, 6], 5),
            ([0, 1, 3, 4, 5, 6], 6),
            ([0, 1, 2, 3, 5, 6], 9),
        ]:
            self.encoder_ring[value] = set([self.segments[i] for i in segment_indices])
            self.decoder_ring[''.join(sorted(self.encoder_ring[value]))] = value

    def decode(self, encoded):
        return self.decoder_ring[''.join(sorted(encoded))]


class Day8Processor(DailyProcessorBase):
    def __init__(self):
        super().__init__(day=8, input_transforms=[Split(), Split(r" \| ")])

    def process(self):
        super().process()
        entries = []
        count_unique = 0
        part2_accumulator = 0

        for line in self.data:
            # count for part 1:
            for output in line[1]:
                if len(output) in (2, 3, 4, 7):
                    count_unique += 1

            decoder = Decoder(line[0] + line[1])
            # ok yeah we don't need to collect these, can just do everything in one loop through...
            entries.append({"inputs": line[0], "outputs": line[1], "decoder": decoder})
            val = 0
            for index, multiplier in [(0, 1000), (1, 100), (2, 10), (3, 1)]:
                val += decoder.decode(line[1][index]) * multiplier
            part2_accumulator += val

        # part 1: count unique values
        print(f"part 1: {count_unique}")
        print(f"part 2: {part2_accumulator}")

if __name__ == "__main__":
    processor = Day8Processor()
    processor.process()