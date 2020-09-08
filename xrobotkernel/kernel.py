"""XRobotKernel."""
from ipykernel.kernelbase import Kernel
from robot.api import get_tokens


class XRobotKernel(Kernel):
    """XRobotKernel."""

    implementation = 'XRobot'
    implementation_version = '0.1'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "XRobot kernel"


    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        output = ''

        for token in get_tokens(code):
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
