import time

from cfx.common.abstracts import Machinery


class VMware(Machinery):
    LABEL = 'vmx_path'

    def start(self):
        time.sleep(3)