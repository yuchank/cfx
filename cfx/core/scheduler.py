import time
import threading

import cfx

from cfx.common.config import Config
from cfx.core.database import Database

machinery = None


class AnalysisManager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.machine = None
        self.db = Database()
        self.task = self.db.view_task(task_id)

    def acquire_machine(self):
        print('acquire machine')
        machine = None

        # start a loop to acquire the a machine to run the analysis on.
        while True:
            if not machinery.available():
                time.sleep(1)
                continue

            machine = machinery.acquire()

            if not machine:
                pass
            else:
                break

        self.machine = machine

    def route_network(self):
        """Enable network routing if desired."""
        # Determine the desired routing strategy (none, internet, VPN).

    def launch_analysis(self):
        print('start analysis')
        self.acquire_machine()

        # Start the machine
        machinery.start()

    def run(self):
        print('analysis run')
        self.launch_analysis()


class Scheduler(object):
    """Tasks Scheduler.

    This class is responsible for the main execution loop of the tool. """
    def __init__(self):
        self.running = True
        self.cfg = Config()
        self.db = Database()

    def initialize(self):
        global machinery

        machinery_name = self.cfg.cfx.machinery

        # Initialize the machine manager.
        machinery = cfx.machinery.plugins['virtualbox']()

        # provide a dictionary with the configuration options to the machine manager instance.
        machinery.set_options(Config(machinery_name))

        machinery.initialize('virtualbox')

    def start(self):
        print('scheduler start')
        self.initialize()

        while self.running:
            time.sleep(1)   # 1 sec
            print('scheduler running')

            analysis = AnalysisManager()
            analysis.start()
