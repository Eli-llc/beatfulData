import argparse
import time

from common.config import ParseYaml
from common.error import ConfKeyNotFound, FragmentFormatError


class Param:

    def __init__(self, conf=None):
        self.config = ParseYaml(conf)
        self.parser = argparse.ArgumentParser(description="Customize your special data")

    def options(self):
        # get config
        time_config: dict = self.config.get_conf("time")
        # data_config: dict = self.config.get_conf("data")
        op_config: dict = self.config.get_conf("output")
        # common params
        self.parser.add_argument('-v', '--verbose', action='store_true', help='show more detail info')
        self.parser.add_argument('-q', '--quite', action='store_true', help='quite standard output')
        # time params
        time_parser = self.parser.add_argument_group("Control time principle of data")
        time_parser.add_argument('--time-fragment', default=time_config.get("time-fragment"), dest="time_fragment",
                                 help="the fragment's name of time")
        time_parser.add_argument('--time-format', type=str, default=time_config.get("time-format"), dest="time_format",
                                 help="specify the format of time."
                                      "Available format for string is along with time module, or you can input"
                                      "timestamp or mill(timestamp)")
        try:
            time_start = time_config.get("time-start")
        except ConfKeyNotFound:
            time_start = int(time.time())
        time_parser.add_argument('--time-start', type=int, default=time_start, dest="time_start",
                                 help="specify the start time. Defaults to current time.")
        time_parser.add_argument('--time-end', type=int, default=time_config.get("time-end"), dest="time_end",
                                 help="specify the end time. Note: it would not take effect while --count provide.")
        time_parser.add_argument('--time-duration', default=time_config.get("time-duration"), dest="time_duration",
                                 type=int, help="how long logs you need to produce. "
                                                "Note: it would not take effect when --time-end is provided.")
        time_parser.add_argument('--time-interval', type=int, default=time_config.get("time-interval"),
                                 dest="time_interval", help="the time gap of two items.")
        time_parser.add_argument('--time-delta', type=int, default=time_config.get("time-delta"), dest="time_delta",
                                 help="adjust the interval, make two items has dynamic time gap.")
        time_parser.add_argument('--count', type=int, default=time_config.get("count"), dest="count",
                                 help="the count of items to produce. Note: It would disable --time-end setting.")
        time_parser.add_argument('--realtime', choices=["true", "false"], default=time_config.get("realtime"),
                                 dest="realtime", help="realtime make two items wait the interval time.")
        # data params
        data_parser = self.parser.add_argument_group("Control data content")
        data_parser.add_argument('--fragments', dest="input_fragments", nargs="*",
                                 help="additional fragments. key-type separate as '=', "
                                      "fragments separate as space")
        # data_parser.add_argument(default=config_fragments, dest="config_fragments", nargs="*", )
        # output params
        op_parser = self.parser.add_argument_group("Control data output")
        # op_fragment: dict = op_config.get("output")
        op_parser.add_argument('--output', action="store_true")
        op_parser.add_argument('--output-type', dest="op_type", default=op_config.get("type"),
                               help="the type of output, current available values: kafka, es, file.")
        op_parser.add_argument('--output-file', dest="op_file", default=op_config.get("file"),
                               help="specify the file path while type setting to file")
        op_parser.add_argument('--output-format', dest="op_format", default=op_config.get("format"),
                               help="specify the format of output contents.")
        op_parser.add_argument('--output-bootstrap', dest="op_bootstrap", default=op_config.get("bootstrap"),
                               help="specify the kafka's bootstrap server while type setting to kafka")
        op_parser.add_argument('--output-topic', dest="op_topic", default=op_config.get("topic"),
                               help="specify the kafka's topic while type setting to kafka")
        op_parser.add_argument('--output-es-hosts', dest="op_es_hosts", default=op_config.get("es-hosts"), type=list,
                               nargs="*", help="specify the ElasticSearch's hosts while type setting to ElasticSearch")
        op_parser.add_argument('--output-index', dest="op_index", default=op_config.get("index"),
                               help="specify the ElasticSearch's index while type setting to ElasticSearch")
        # return parameters
        args = self.parser.parse_args()
        return self.merge_fragments(args)

    def merge_fragments(self, args):
        """
        supply command line fragments to args.fragments
        :param args:
        :return:
        """
        data_config: dict = self.config.get_conf("data")
        # fragments defined in config file
        config_fragments: dict = data_config.get("fragments")
        input_fragments: list = args.input_fragments
        if input_fragments:
            # merge fragments
            try:
                for frag_str in input_fragments:  # raise TypeError
                    frag = frag_str.split("=")
                    key = frag[0]  # raise IndexError
                    config_fragments[key] = frag[1]  # raise IndexError
            except (IndexError, TypeError):
                message = "The standard input fragments must have format like key=type!"
                raise FragmentFormatError(message)
        args.fragments = config_fragments
        return args


if __name__ == '__main__':
    s = Param().options()
    s.__dict__["liucun"] = "liucun"
    print(s.__dict__)
    print(s.liucun)