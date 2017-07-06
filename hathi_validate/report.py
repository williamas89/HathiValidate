import abc
import typing
import itertools
import sys

from . import result


class AbsReport(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self, results: typing.List[result.Result]):
        pass


class Report:
    def __init__(self, report_strategy: AbsReport) -> None:
        self._strategy = report_strategy

    def generate(self, results: typing.List[result.Result]):
        self._strategy.generate(results)


class ConsoleReport(AbsReport):
    def __init__(self, file=sys.stdout):
        self.file = file

    def generate(self, results: typing.List[result.Result]):
        sorted_results = sorted(results, key=lambda r: r.source)
        grouped = itertools.groupby(sorted_results, key=lambda r: r.source)
        print("\nValidation Results:")
        print("===================")
        for source_group in grouped:
            print("\n{}".format(source_group[0]), file=self.file)
            for i, res in enumerate(source_group[1]):
                print("{}: {}".format(i + 1, res.message))
        print("===================")


class TextReport(AbsReport):
    def __init__(self, file):
        self.file = file

    def generate(self, results: typing.List[result.Result]):
        sorted_results = sorted(results, key=lambda r: r.source)
        grouped = itertools.groupby(sorted_results, key=lambda r: r.source)
        with open(self.file, "w", encoding="utf8") as w:
            w.write("Validation Results\n\n")
            for source_group in grouped:
                w.write("\n{}\n".format(source_group[0]))
                for res in source_group[1]:
                    w.write("{}\n".format(res.message))
