class Machinery(object):
    def __init__(self):
        print('Machinery init')

    def initialize(self, module_name):
        pass

    def availables(self):
        return True

    def acquire(self):
        pass

    def start(self):
        raise NotImplementedError
