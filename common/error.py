from common.log import logger


class MyError(Exception):
    def __init__(self, message):
        self.message = message
        logger.error(self.message)

    def __str__(self):
        return repr(self.message)


class ConfKeyNotFound(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)


class FormatError(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)


class MethodError(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)


class CompareResultError(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)


class FileNotFoundError2(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)


class NotFoundCaseId(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)


class FileContentError(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)


class JsonMatchError(MyError):
    def __init__(self, message, e=None):
        logger.warning("Caught Error:\n{}".format(e))
        MyError.__init__(self, message)


class ClearDataError(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)


class SaveConfigError(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)


class ModifyRuleError(MyError):
    def __init__(self, message):
        MyError.__init__(self, message)
