import random
from faker import Faker

from common.error import DataTypeNotSupportError, FloatPrecisionError


class RawDataFactory:
    def __init__(self):
        self.faker = Faker()
        self.map = {
            "sentence": self._get_sentence,
            "word": self._get_word,
            "mul-word": self._get_mul_word,
            "int": self._get_numeral,
            "float": self._get_numeral,
            "severity": self._get_severity
        }

    def get_data(self, key, num, en='zh_CN', scope=(1, 100), precision=2):
        # get 1 from 5 category [sentence, word, mul_word, int, float]
        if key in self.map:
            func = self.map.get(key)
            return func(num=num, en=en, scope=scope, precision=precision)
        else:
            message = "Data type: {key} not defined.".format(key=key)
            raise DataTypeNotSupportError(message)

    @staticmethod
    def _get_sentence(num, en='zh_CN', scope=(1, 100), precision=2) -> list:
        module = [
            "AM Container for appattempt_1465808152295_000001 exited with exitCode: -103 " +
            "For more detailed output check application tracking page",
            "CPU-dict将 zookeeper-3.4.8 文件夹复制到另外error1两个节点下 today's weather is {}",
            "os-network  channel worker1 的 myid 文件内容为 {} end",
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
    def _get_word(num, en='zh_CN', scope=(1, 100), precision=2) -> list:
        faker = Faker(en)
        return [faker.province() for _ in range(num)]

    @staticmethod
    def _get_mul_word(num, en='zh_CN', scope=(1, 100), precision=2) -> list:
        faker = Faker(en)
        return [faker.name() for _ in range(num)]

    @staticmethod
    def _get_severity(num, en='zh_CN', scope=(1, 100), precision=2) -> list:
        severities = [10, 20, 30, 40, 50, 60]
        return [random.choice(severities) for _ in range(num)]

    @staticmethod
    def _get_numeral(num, en='zh_CN', scope=(1, 100), precision=None) -> list:
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
                raise FloatPrecisionError("Float precision must be int or None")
            result_len = len(result)
            if result_len >= num:
                break
        return list(result)

