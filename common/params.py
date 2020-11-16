import argparse
import time

from common.config import ParseYaml
from common.error import ConfKeyNotFound


class Param:

    def __init__(self, conf=None):
        self.config = ParseYaml(conf)
        self.parser = argparse.ArgumentParser(description="Customize your special data")

    def options(self):
        # get config
        time_config: dict = self.config.get_conf("time")
        data_config: dict = self.config.get_conf("data")
        op_config: dict = self.config.get_conf("output")
        # common params
        self.parser.add_argument('--verbose', '-v', action='store_true', help='show more detail info')
        # time params
        time_parser = self.parser.add_argument_group("Control time principle of data")
        time_parser.add_argument('--time-fragment', type=str, default=time_config.get("time-fragment"),
                                 dest="time_fragment")
        time_parser.add_argument('--time-format', type=str, default=time_config.get("time-format"), dest="time_format")
        try:
            time_start = time_config.get("time-start")
        except ConfKeyNotFound:
            time_start = int(time.time())
        time_parser.add_argument('--time-start', type=int, default=time_start, dest="time_start")
        time_parser.add_argument('--time-end', type=int, default=time_config.get("time-end"), dest="time_end")
        time_parser.add_argument('--time-duration', type=int, default=time_config.get("time-duration"),
                                 dest="time_duration")
        time_parser.add_argument('--time-interval', type=int, default=time_config.get("time-interval"),
                                 dest="time_interval")
        time_parser.add_argument('--time-delta', type=int, default=time_config.get("time-delta"), dest="time_delta")
        time_parser.add_argument('--count', type=int, default=time_config.get("count"), dest="count")
        time_parser.add_argument('--realtime', choices=["true", "false"],
                                 default=time_config.get("realtime"), dest="realtime")
        # data params
        data_parser = self.parser.add_argument_group("Control data content")
        data_fragment = data_config.get("fragments")
        # data_parser.add_argument('-d', help="not functional")
        data_parser.add_argument('--fragments', dest="input_fragments",
                                 help="additional fragments. key-type separate as '=', "
                                      "fragments separate as space")
        data_parser.add_argument(default=data_fragment, dest="config_fragments", nargs="*")
        # output params
        op_parser = self.parser.add_argument_group("Control data output")
        op_fragment: list = op_config.get("output")
        op_parser.add_argument('--output', action="store_true")
        op_parser.add_argument('--output-type', dest="op_type")
        op_parser.add_argument('--output-path', dest="op_path")
        # return parameters
        return self.parser.parse_args()
