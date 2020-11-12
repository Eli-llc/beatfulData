from common.params import Param


class DataFactory:
    def __init__(self):
        pass

    def run(self):
        pass

    def json(self):
        single_data = ["{", "}"]
        return single_data

    def xml(self):
        pass


if __name__ == '__main__':
    args = Param().options()
    print("start time", args.time_start)
