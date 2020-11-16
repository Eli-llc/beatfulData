from common.error import UnknownOutPutType
from common.params import Param
from tools.compose_data import ComposeData
from tools.output_data import OutputData
from tools.raw_data import RawDataFactory


class CreateData:
    def __init__(self):
        self.param = Param()
        self.args = self.param.options()
        self.raw_data = RawDataFactory()
        self.comp_data = ComposeData(self.args, self.raw_data)
        self.op_data = OutputData(self.param.config)

    def run(self):
        """
        1. get all common fragments
        2. get time fragment
        3. loop writing data to file or kafka or es
            judge time in condition
            get formatted time
            add time to common fragments
            write complete contents to destination
        4. close
        :return:
        """
        all_fragments = self.comp_data.merge_fragments()
        file_type = self.args.op_type
        for time_value in self.comp_data.get_time():
            fragment_with_value = self.comp_data.fill_fragment_values(all_fragments)
            fragment_with_value.update(time_value)
            if file_type.upper() == "JSON":
                self.op_data.to_json(fragment_with_value, self.op_data.fp)
            elif file_type.upper() == "CSV":
                self.op_data.to_csv(fragment_with_value)
            elif file_type.upper() == "KAFKA":
                self.op_data.to_kafka(fragment_with_value)
            elif "ES" in file_type.upper() or "ElasticSearch".upper() in file_type.upper():
                self.op_data.to_es(fragment_with_value)
            else:
                message = "Could not handle output type {}!".format(file_type)
                raise UnknownOutPutType(message)
        self.op_data.close()


if __name__ == '__main__':
    ins = CreateData()
    ins.run()
