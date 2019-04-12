import click
import logging
import os
import shutil
import sys

import cfx

from cfx.common.exceptions import CFXCriticalError
from cfx.common.utils import exception_message
from cfx.core.database import Database
from cfx.core.scheduler import Scheduler

from cfx.misc import (
    cwd, decide_cwd, drop_privileges
)

log = logging.getLogger('cfx')


def cfx_create(username=None, cfg=None, quiet=False):
    """
    Create a new CFX Working Directory
    """

    if not os.path.exists(cwd('.cwd', private=True)):
        print("The cfx/private/.cwd file is missing. Please run "
              "'python setup.py sdist' before 'pip install ...'!")
        return

    if not os.path.isdir(cwd()):
        os.mkdir(cwd())

    def _ignore_pyc(src, names):
        """Don't copy .pyc files."""
        return [name for name in names if name.endswith('.pyc')]

    # The following effectively nops the first os.makedirs() call that
    # shutil.copytree() does as we've already created the destination
    # directory ourselves (assuming it didn't exist already).
    orig_makedirs = shutil.os.makedirs

    def _ignore_first_makedirs(dst):
        shutil.os.makedirs = orig_makedirs

    shutil.os.makedirs = _ignore_first_makedirs

    shutil.copytree(os.path.join(cfx.__path__[0], 'data'), cwd(), symlinks=True, ignore=_ignore_pyc)

    # Drop our version of the CWD.
    # TODO not yet implemented
    # our_version = open(cwd('.cwd', private=True), 'rb').read()
    # open(cwd('.cwd'), 'wb').write(our_version)

    # Write the supervisord.conf configuration file.


def cfx_init(level, ctx, cfg=None):
    """
    Initialize Cuckoo configuration.
    """

    # It would appear this is the first time CFX is being run (on this CFX Working Directory anyway).
    if not os.path.isdir(cwd()) or not os.listdir(cwd()):
        cfx_create(ctx.user, cfg)
        sys.exit(0)

    Database().connect()


def cfx_main():
    print('cfx_main')
    scheduler = Scheduler()
    scheduler.start()


@click.group(invoke_without_command=True)
@click.option('-d', '--debug', is_flag=True, help='Enable verbose logging')
@click.option('-q', '--quiet', is_flag=True, help='Only log warnings and critical messages')
@click.option('--nolog', is_flag=True, help='Don\'t log to file.')
@click.option('-m', '--maxcount', default=0, help='Maximum number of analyses to process')
@click.option('--user', help='Drop privileges to this user')
@click.option('--cwd', help='CFX Working Directory')
@click.pass_context
def main(ctx, debug, quiet, nolog, maxcount, user, cwd):
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

    # Drop privileges.
    user and drop_privileges(user)
    ctx.user = user

    ctx.log = not nolog

    if quiet:
        level = logging.WARN
    elif debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    ctx.level = level

    # A subcommand will be invoked, so don't run CFX itself.
    if ctx.invoked_subcommand:
        return

    try:
        cfx_init(level, ctx)
        cfx_main(maxcount)
    except CFXCriticalError as e:
        log.critical('{0}: {1}'.format(e.__class__.__name__, e))
        sys.exit(1)
    except SystemExit as e:
        pass
    except Exception as e:
        # Deal with an unhandled exception.
        sys.stderr.write(exception_message())
        log.exception('{0}: {1}'.format(e.__class__.__name__, e))
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
