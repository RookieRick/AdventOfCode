from AdventOfCode.util import input_parser


class DailyProcessorBase:
    def __init__(self, day: int, input_transforms=None, input_blob=False, debug=False):
        self.day = day
        self.input_transforms = input_transforms  # input_parser will handle None-->[] as needed
        self.input_blob = input_blob
        self.debug = debug
        self.data = None

    def print_debug(self, message):
        if self.debug:
            print(message() if callable(message) else message)

    def _get_input(self):
        filename = f"./raw_inputs/day{self.day}{'_debug' if self.debug else ''}.txt"
        self.data = input_parser.parse(filename, transforms=self.input_transforms, blob=self.input_blob)
        return self.data

    def process(self):
        self._get_input()

        # override this method (and make sure to call super first to get input) with the actual daily processing
        pass


