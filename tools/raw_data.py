import random
import os
from faker import Faker

from common.error import DataTypeNotSupportError, FloatPrecisionError, FileNotFoundError2
from common.log import logger


class RawDataFactory:
    def __init__(self):
        self.faker = Faker()
        self.map = {
            "sentence": self._get_sentence,
            "word": self._get_word,
            "mul-word": self._get_mul_word,
            "int": self._get_numeral,
            "float": self._get_numeral,
            "severity": self._get_severity,
            "file": self.read_file
        }
        logger.debug(f"Class RawDataFactory with map:\n{self.map}")

    def get_data(self, key, **kwargs):
        # get 1 from 5 category [sentence, word, mul_word, int, float]
        if key in self.map:
            func = self.map.get(key)
            data = func(key=key, **kwargs)
            logger.debug(f"Current key is {key}, return data's type is {type(data)}, content is\n{data}")
            return data
        else:
            message = "Data type: {key} not defined.".format(key=key)
            raise DataTypeNotSupportError(message)

    @staticmethod
    def _get_sentence(**kwargs) -> list:
        num = kwargs.get("num", 10)
        module = [
            "AM Container for app attempt_1465808152295_000001 exited with exitCode: -103 " +
            "For more detailed output check application tracking page",
            "CPU-dict将 zookeeper-3.4.8 文件夹复制到另外error1两个节点下 today's weather is {}",
            "os-network  channel worker1 的 my id 文件内容为 {} end",
            "elasticSearch [DefaultQuartzScheduler_Worker-10] {} com.eoitek.dc.connect.kafka.KafkaInput",
            "存储硬件 information technology and services company"
        ]
        replace_words = [
            "rain",
            "snow",
            "sunny",
            "wind",
            "cloud"
        ]
        return [random.choice(module).format(random.choice(replace_words)) for _ in range(num)]

    @staticmethod
    def _get_word(**kwargs) -> list:
        num = kwargs.get("num", 10)
        en = kwargs.get("en", "zh_CN")
        faker = Faker(en)
        return [faker.province() for _ in range(num)]

    @staticmethod
    def _get_mul_word(**kwargs) -> list:
        num = kwargs.get("num", 10)
        en = kwargs.get("en", "zh_CN")
        faker = Faker(en)
        return [faker.name() for _ in range(num)]

    @staticmethod
    def _get_severity(**kwargs) -> list:
        num = kwargs.get("num", 10)
        severities = [10, 20, 30, 40, 50, 60]
        return [random.choice(severities) for _ in range(num)]

    @staticmethod
    def _get_numeral(**kwargs) -> list:
        num = kwargs.get("num", 10)
        scope = kwargs.get("scope", (1, 100))
        precision = kwargs.get("precision", 2)
        if len(scope) == 2:
            boot = scope[0]
            root = scope[1]
            if root - boot <= num:
                raise RuntimeError
        else:
            boot = 0
            root = boot + num + 1
        result = set()
        while True:
            if not precision:
                result.add(random.randint(boot, root))
            elif isinstance(precision, int):
                base = random.randrange(boot, root)
                delta = round(random.random(), abs(precision))
                result.add(base + delta)
            else:
                raise FloatPrecisionError("Float precision must be Int or None")
            result_len = len(result)
            if result_len >= num:
                break
        return list(result)

    @staticmethod
    def read_file(key, **kwargs):
        num = kwargs.get("num", -1)
        file_name = os.path.abspath(os.path.join(os.path.curdir, key))
        try:
            with open(file_name) as fp:
                lines = fp.readlines()
        except FileNotFoundError:
            message = "No such file or directory: {}".format(file_name)
            raise FileNotFoundError2(message)
        if num > len(lines):
            return lines
        return lines[:num]
