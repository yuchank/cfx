import time
import threading

import cfx

machinery = None


class AnalysisManager(threading.Thread):

    def __init__(self):
        self.machine = None

    def acquire_machine(self):
        print('acquire machine')
        machine = None

        # start a loop to acquire the a machine to run the analysis on.
        while True:
            if not machinery.availables():
                time.sleep(1)
                continue

            machine = machinery.acquire()

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
    def __init__(self):
        print('Scheduler')
        self.running = True

    def initialize(self):
        global machinery

        # Initialize the machine manager.
        machinery = cfx.machinery.plugins['virtualbox']()

        machinery.initialize('virtualbox')

    def start(self):
        print('scheduler start')
        self.initialize()

        while self.running:
            time.sleep(1)   # 1 sec
            print('scheduler running')

            analysis = AnalysisManager()
            analysis.start()
