import logging
import argparse

import sys

from hathi_validate import package, process, configure_logging, report
import hathi_validate


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version',
        action='version',
        version=hathi_validate.__version__)
    parser.add_argument("path", help="Path to the hathipackages")
    debug_group = parser.add_argument_group("Debug")
    debug_group.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")
    debug_group.add_argument("--log-debug", dest="log_debug", help="Save debug information to a file")
    return parser


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    parser = get_parser()
    args = parser.parse_args()

    configure_logging.configure_logger(debug_mode=args.debug, log_file=args.log_debug)

    errors = []
    for pkg in package.get_dirs(args.path):
        logger.info("Checking {}".format(pkg))
        errors += process.process_directory(pkg)

    console_reporter = report.Report(report.ConsoleReport())
    text_reporter = report.Report(report.TextReport("dummy.txt"))
    console_reporter.generate(errors)
    text_reporter.generate(errors)

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        import pytest  # type: ignore

        sys.exit(pytest.main(sys.argv[2:]))
    else:
        main()
