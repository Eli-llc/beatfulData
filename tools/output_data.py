import json


class OutputData:
    def __init__(self, args):
        # self.args_dict = args
        # file_name = self.args_dict.get("output").get("file")
        file_name = args.get_conf("output").get("file")
        self.fp = open(file_name, "w")

    @staticmethod
    def to_json(fragments_values, fp):
        """
        write fragments_values to json file
        :param fragments_values: a dict contains contents to write to file
        :param fp: file point object
        :return: None
        """
        content_string = json.dumps(fragments_values, ensure_ascii=False)
        fp.write(content_string)
        fp.write("\n")

    def to_csv(self, fragments_values):
        pass

    def to_kafka(self, fragment_with_value):
        pass

    def to_es(self, fragment_with_value):
        pass

    def close(self):
        self.fp.close()
