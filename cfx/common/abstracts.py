from cfx.core.database import Database


class Machinery(object):

    def __init__(self):
        self.options = None
        self.db = Database()

    def set_options(self, options):
        """ Set machine manager options
        :param options:
        :return:
        """
        self.options = options

    def initialize(self, module_name):
        """Read, load and verify machines configuration.
        @param module_name: module name.
        """
        # Load.
        self._initialize(module_name)

    def _initialize(self, module_name):
        """Read configuration.
        @param module_name: module name.
        """


    def available(self):
        pass

    def acquire(self):
        pass

    def start(self):
        raise NotImplementedError
