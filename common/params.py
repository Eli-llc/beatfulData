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
        config = self.config
        parser = self.parser
        time_config: dict = config.get_conf("time")
        data_config: dict = config.get_conf("data")
        op_config: dict = config.get_conf("output")
        # common params
        parser.add_argument('--verbose', '-v', action='store_true', help='show more detail info')
        # time params
        time_parser = parser.add_argument_group("Control time principle of data")
        time_parser.add_argument('--time-fragment', type=str, default=time_config.get("time-fragment"),
                                 dest="time_fragment")
        try:
            time_start = time_config.get("time-start")
        except ConfKeyNotFound:
            time_start = int(time.time())
        time_parser.add_argument('--time-start', type=int, default="time_start")
        time_parser.add_argument('--time-end', type=int, default=time_config.get("time-end"), dest="time_end")
        time_parser.add_argument('--time-duration', type=int, default=time_config.get("time-duration"),
                                 dest="time_duration")
        time_parser.add_argument('--time-interval', type=int, default=time_config.get("time-interval"),
                                 dest="time_interval")
        time_parser.add_argument('--time-delta', type=int, default=time_config.get("time-delta"), dest="time_delta")
        # data params
        data_parser = parser.add_argument_group("Control data content")
        data_fragment: list = data_config.get("fragments")
        data_parser.add_argument('-d', help="not functional")
        # output params
        op_parser = parser.add_argument_group("Control data output")
        op_fragment: list = op_config.get("output")
        op_parser.add_argument('--output', action="store_true")
        op_parser.add_argument('--output-type', choices=["file", "kafka", "es"], dest="op_type")
        op_parser.add_argument('--output-path', dest="op_path")
        # return parameters
        return parser.parse_args()


args = Param().options()
