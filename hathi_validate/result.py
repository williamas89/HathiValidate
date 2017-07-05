import abc


class Result:
    message = ""

    def __init__(self, result_type):
        self.result_type = result_type


class ResultSummary:
    results = []
    source = None

    def __add__(self, other):
        self.results.append(other)


class AbsResultBuilder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_new_summary(self):
        pass

    @abc.abstractmethod
    def add_result(self, result: Result):
        pass

    @abc.abstractmethod
    def get_summary(self) -> ResultSummary:
        pass

    @abc.abstractmethod
    def set_source(self, source):
        pass


class ResultSummaryBuilder(AbsResultBuilder):
    summary = None
    source = None

    def create_new_summary(self):
        self.summary = ResultSummary()

    def add_result(self, result: Result):
        self.summary += result

    def get_summary(self) -> ResultSummary:
        return self.summary

    def set_source(self, source):
        self.source = source


class SummaryDirector:
    def __init__(self, source):
        self.builder = ResultSummaryBuilder()
        self.builder.create_new_summary()
        self.builder.source = source

    def add_error(self, message):
        new_error = Result("error")
        new_error.message = message
        self.builder.add_result(new_error)

    def construct(self)->ResultSummary:
        return self.builder.get_summary()
