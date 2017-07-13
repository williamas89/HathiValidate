import argparse
import logging
import os
import threading

from script_gui import SimpleGui, AbsScript
import hathi_validate
from hathi_validate import package, process, configure_logging, report
from PyQt5 import QtWidgets

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version',
        action='version',
        version=hathi_validate.__version__)
    parser.add_argument("path", nargs="?", help="Path to the hathipackages")
    parser.add_argument("--save-report", dest="report_name", help="Save report to a file")
    debug_group = parser.add_argument_group("Debug")
    debug_group.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")
    debug_group.add_argument("--log-debug", dest="log_debug", help="Save debug information to a file")
    parser.add_argument("--gui", action='store_true', help="Experimental gui")
    return parser


class SimpleGui2(SimpleGui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # continue_anyways = self.inform_experimental()
        # if not continue_anyways:
        #     print("closing")


    def inform_experimental(self):
        warning_message = """The GUI version is currently experimental. 
Are you sure you want to continue?
        """
        reply = QtWidgets.QMessageBox.question(self, "Warning: Experimental Feature", warning_message, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            return True
        elif reply == QtWidgets.QMessageBox.No:
            return False
        else:
            raise Exception("Invalid response")

class HathiValidateScript(AbsScript):

    def _script(self):
        errors = []
        path = self.args["Path"].value
        for i, pkg in enumerate(package.get_dirs(path)):
            if self._abort_flag.is_set():
                break
            self.logger.info("{}) Checking {}".format(i +1, pkg))
            errors += process.process_directory(pkg)
        self.logger.info("Checking Finished")
        console_reporter = report.Report(report.LogReport(self.logger))
        console_reporter.generate(errors)
        self.announce_ended()



    def run(self):
        self._script()

    def __init__(self, args):
        super().__init__()
        self.logger = logging.getLogger(__package__)
        default_path = args.path if args.path else ""
        self.args.add_required(name="Path", default=default_path, help="Path to the Hathi Packages", validate=lambda user_input: os.path.isdir(user_input))


    @property
    def title(self) -> str:
        return hathi_validate.FULL_TITLE

    def start(self):
        self.t = threading.Thread(target=self._script, daemon=True)
        self.t.start()


    #

def main():
    parser = get_parser()
    args = parser.parse_args()
    configure_logging.configure_logger(debug_mode=args.debug)
    script = HathiValidateScript(args)
    app = SimpleGui2(script)

    if args.debug or app.inform_experimental():
        app.load_logger()
        app.display()
    else:
        print("Exit")


if __name__ == '__main__':
    main()
