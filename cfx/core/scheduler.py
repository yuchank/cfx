import time
import threading

import cfx

from cfx.common.config import Config
from cfx.core.database import Database

machinery = None


class AnalysisManager(threading.Thread):
    """
    Analysis Manager.

    This class handles the full analysis process for a given task. It takes
    care of selecting the analysis machine, preparing the configuration and
    interacting with the guest agent and analyzer components to launch and
    complete the analysis and store, process and report its results.
    """

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

    This class is responsible for the main execution loop of the tool.
    It prepares the analysis machines and keep waiting and loading for new analysis tasks.
    Whenever a new task is available, it launches AnalysisManager which will
    take care of running the full analysis process and operating with the assigned analysis machine.
    """
    def __init__(self, maxcount=None):
        self.running = True
        self.cfg = Config()
        self.db = Database()
        self.maxcount = maxcount
        self.total_analysis_count = 0

    def initialize(self):
        global machinery

        machinery_name = self.cfg.cfx.machinery

        # Initialize the machine manager.
        machinery = cfx.machinery.plugins['virtualbox']()

        # provide a dictionary with the configuration options to the machine manager instance.
        machinery.set_options(Config(machinery_name))

        machinery.initialize('virtualbox')

    def stop(self):
        """Stop scheduler"""
        self.running = False
        # Shutdown machine manager (used to kill machines that still alive).
        machinery.shutdown()

    def start(self):
        self.initialize()

        while self.running:
            time.sleep(1)   # 1 sec

            # Fetch a pending analysis task.
            task, available = None, False
            for machine in self.db.get_available_machines():
                task = self.db.fetch(machine=machine.name)

            analysis = AnalysisManager()
            analysis.start()
