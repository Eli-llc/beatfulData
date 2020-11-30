#!/Users/eoitek/PycharmProjects/MyFrame/venv/bin/python3

from common.params import Param
from tools.compose_data import ComposeData
from tools.output_data import OutputData
from tools.raw_data import RawDataFactory
from common.log import logger


class CreateData:
    def __init__(self):
        self.param = Param()
        self.args = self.param.options()
        logger.debug("All args' final value is:\n{}".format(self.args.__dict__))
        self.raw_data = RawDataFactory()
        self.comp_data = ComposeData(self.args, self.raw_data)

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
        all_fragments = self.args.fragments
        logger.info(f"All fragments with type is\n{all_fragments}")
        op_type = self.args.op_type.upper()
        logger.info(f"output type is {op_type}")
        with OutputData(self.args) as op_data:
            # op_data.op_format = self.args.op_format
            for time_value in self.comp_data.get_time():
                fragment_with_value = self.comp_data.fill_fragment_values(all_fragments)
                fragment_with_value.update(time_value)
                # logger.debug(f"All fragments with value is:\n{fragment_with_value}")
                op_data.to_dest(op_type, fragment_with_value)


if __name__ == '__main__':
    ins = CreateData()
    ins.run()
