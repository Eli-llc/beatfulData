import random
from collections import Iterator

from faker import Faker


class DataFactory:
    def __init__(self):
        self.faker = Faker()

    def get_data(self, key):
        pass

    @staticmethod
    def get_sentence(num, en='zh_CN') -> Iterator:
        faker = Faker(en)
        return (faker.address for _ in range(num))

    @staticmethod
    def get_word(num, en='zh_CN') -> Iterator:
        faker = Faker(en)
        return (faker.province() for _ in range(num))

    @staticmethod
    def get_mul_word(num, en='zh_CN') -> Iterator:
        faker = Faker(en)
        return (faker.name for _ in range(num))

    @staticmethod
    def get_int(num, scope=(), category=int):
        if len(scope) == 2:
            boot = scope[0]
            root = scope[1]
            if root - boot <= num:
                raise RuntimeError
        else:
            boot = 0
            root = boot + num + 1
        result = []
        while True:
            if category is int:
                result.append(random.randint(boot, root))
            elif category is float:
                base = random.randrange(boot, root)
                delta = random.random()
                result.append(base + delta)
            result_len = len(set(result))
            if result_len >= num:
                break
        return result

    # @staticmethod
    # def get_numetric(num, scope=(), type=int):
    #     if len(scope) == 2:
    #         boot = scope[0]
    #         root = scope[1]
    #         if root - boot <= num:
    #             raise RuntimeError
    #     else:
    #         boot = 0
    #         root = boot + num + 1
    #     result = []
    #     while True:
    #         result.append(random.randint(boot, root))
    #         result_len = len(set(result))
    #         if result_len >= num:
    #             break
    #     return result


if __name__ == '__main__':
    a = int
    print(a is int)
