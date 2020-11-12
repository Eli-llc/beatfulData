import random
from collections import Iterator

from faker import Faker

from common.error import DataTypeNotSupportError


class DataFactory:
    def __init__(self):
        self.faker = Faker()

    def get_data(self, key, num, en='zh_CN', scope=(1, 100)):
        # get 1 from 5 category [sentence, word, mul_word, int, float]
        if key == "sentence":
            return self.get_sentence(num, en)
        elif key == "word":
            return self.get_word(num, en)
        elif key == "mul_word":
            return self.get_mul_word(num, en)
        elif key in ["int", "float"]:
            return self.get_int(num, scope, key)
        else:
            message = "Data type: {key} not support." \
                      "Available values [\"sentence\", \"word\", \"mul_word\", \"int\", \"float\"]".format(key=key)
            raise DataTypeNotSupportError(message)

    @staticmethod
    def get_sentence(num, en='zh_CN') -> Iterator:
        faker = Faker(en)
        return (faker.address() for _ in range(num))

    @staticmethod
    def get_word(num, en='zh_CN') -> Iterator:
        faker = Faker(en)
        return (faker.province() for _ in range(num))

    @staticmethod
    def get_mul_word(num, en='zh_CN') -> Iterator:
        faker = Faker(en)
        return (faker.name() for _ in range(num))

    @staticmethod
    def get_int(num, scope=(), category="int", precision=2):
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
            if category is "int":
                result.add(random.randint(boot, root))
            elif category is "float":
                base = random.randrange(boot, root)
                delta = round(random.random(), precision)
                result.add(base + delta)
            result_len = len(result)
            if result_len >= num:
                break
        return result


if __name__ == '__main__':
    factory = DataFactory()
    result = factory.get_data(key="float", num=10)
    for x in result:
        print(x)
