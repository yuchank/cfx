from cfx.core.database import Database
from cfx.core.scheduler import Scheduler

from cfx.misc import (
    cwd, decide_cwd
)


def cfx_init():
    print('cfx_init')

    Database().connect()


def cfx_main():
    print('cfx_main')
    scheduler = Scheduler()
    scheduler.start()


def main(cwd):
    """
    Invokes the Cuckoo daemon or one of its sub commands.

    To be able to use different Cuckoo configurations on the same machine with
    the same Cuckoo installation, we use the so-called Cuckoo Working Directory (aka 'CWD').
    A default CWD is available, but may be overridden through the following options
    - listed in order of precedence.

    \b
    *
    *
    *
    *
    *
    """
    decide_cwd(cwd)

    cfx_init()
    cfx_main()


if __name__ == '__main__':
    main()
