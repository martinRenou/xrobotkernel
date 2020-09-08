"""XRobotKernel."""
from ipykernel.kernelbase import Kernel
from robot.parsing.lexer.context import TestCaseFileContext
from robot.parsing.lexer.lexer import Lexer


class XRobotKernel(Kernel):
    """XRobotKernel."""

    implementation = 'XRobot'
    implementation_version = '0.1'
    language = 'robot'
    language_version = '0.1'
    language_info = {
        'name': 'robot',
        'mimetype': 'text/plain',
        'file_extension': '.robot',
    }
    banner = "XRobot kernel"


    def __init__(self, *args, **kwargs):
        self.context = TestCaseFileContext()
        self.lexer = Lexer(self.context, False, False)
        self.tokens = []

        super(XRobotKernel, self).__init__(*args, **kwargs)


    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.lexer.input(code)

        output = ''

        all_tokens = list(self.lexer.get_tokens())
        new_tokens = all_tokens[len(self.tokens):]

        self.tokens = all_tokens

        for token in new_tokens:
            output += repr(token) + '\n'

        if not silent:
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }
