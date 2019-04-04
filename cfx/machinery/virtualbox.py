import subprocess

from cfx.common.abstracts import Machinery

from cfx.misc import Popen


class VirtualBox(Machinery):
    RUNNING = 'running'

    def start(self, label, task):
        args = [
            self.options.virtualbox.path, 'startvm', label, '--type', self.options.virtualbox.mode
        ]
        _, err = Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            close_fds=True
        ).communicate()

