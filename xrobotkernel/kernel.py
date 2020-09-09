"""XRobotKernel."""

from io import StringIO
import os
from tempfile import TemporaryDirectory

from ipykernel.kernelbase import Kernel

from robot.api import get_model
from robot.running.model import TestSuite
from robot.running.builder.testsettings import TestDefaults
from robot.running.builder.parsers import ErrorReporter
from robot.running.builder.transformers import SettingsBuilder, SuiteBuilder
from robot.model.itemlist import ItemList


class XRobotKernel(Kernel):
    """XRobotKernel."""

    implementation = 'XRobot'
    implementation_version = '0.1'
    language = 'robot'
    language_version = '0.1'
    language_info = {
        'name': 'XRobot',
        'mimetype': 'text/x-robotframework',
        'file_extension': '.robot',
        'codemirror_mode': 'robotframework',
        'pygments_lexer': 'robotframework',
    }
    banner = "XRobot kernel"


    def __init__(self, *args, **kwargs):
        self.suite = TestSuite(name="Jupyter", source=os.getcwd())
        self.defaults = TestDefaults(None)

        super(XRobotKernel, self).__init__(*args, **kwargs)


    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        # Compile AST
        model = get_model(
            StringIO(code),
            data_only=False,
            curdir=os.getcwd().replace("\\", "\\\\"),
        )
        ErrorReporter(code).visit(model)
        SettingsBuilder(self.suite, self.defaults).visit(model)
        SuiteBuilder(self.suite, self.defaults).visit(model)

        # Strip variables/keyword duplicates
        self.suite.resource.variables._items = self.strip_duplicates(self.suite.resource.variables)
        self.suite.resource.keywords._items = self.strip_duplicates(self.suite.resource.keywords)

        # Execute suite
        stdout = StringIO()
        with TemporaryDirectory() as path:
            result = self.suite.run(outputdir=path, stdout=stdout)

        # Remove tests run so far,
        # this is needed so that we don't run them again in the next execution
        self.suite.tests._items = []

        if not silent:
            stats = result.statistics

            output = 'Failed tests: {}; Passed tests: {}; Total: {};'.format(
                stats.total.critical.failed, stats.total.critical.passed,
                stats.total.critical.failed + stats.total.critical.passed
            )

            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def strip_duplicates(self, items):
        """Remove duplicates from a list of variables/keywords."""
        new_items = {}
        for item in items:
            new_items[item.name] = item
        return list(new_items.values())
