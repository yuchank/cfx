from cfx.core.database import Database
from cfx.core.scheduler import Scheduler


def cfx_init():
    print('cfx_init')

    Database().connect()


def cfx_main():
    print('cfx_main')
    scheduler = Scheduler()
    scheduler.start()


def main():
    print('main')
    cfx_init()
    cfx_main()


if __name__ == '__main__':
    main()
