import os
import subprocess
import sys

try:
    import pwd
    HAVE_PWD = True
except ImportError:
    HAVE_PWD = False

from cfx.common.exceptions import CFXStartupError


# Cuckoo Working Directory base path.
_root = None
_raw = None


def set_cwd(path, raw=None):
    global _root, _raw
    _root = path
    _raw = raw


def cwd(*args, **kwargs):
    """
    Returns absolute path to this file in the Cuckoo Working Directory or
    optionally - when private=True has been passed along - to our private
    Cuckoo Working Directory which is not configurable.
    """
    return os.path.join(_root, *args)


def decide_cwd(cwd=None, exists=False):
    """
    Decides and sets the CWD, optionally checks if it's a valid CWD.
    """
    if not cwd:
        cwd = os.environ.get('CFX_CWD')

    if not cwd:
        cwd = os.environ.get('CFX')

    if not cwd and os.path.exists('.cwd'):
        cwd = '.'

    if not cwd:
        cwd = '~/.cfx'

    dirpath = os.path.abspath(os.path.expanduser(cwd))
    if exists:
        if not os.path.exists(dirpath):
            raise CFXStartupError(
                'Unable to start this CFX command as the provided CWD (%r) '
                'is not present!' % dirpath
            )

        if not os.path.exists(os.path.join(dirpath, '.cwd')):
            raise CFXStartupError(
                'Unable to start this CFX command as the provided CWD (%r) '
                'is not present!' % dirpath
            )

    set_cwd(dirpath, raw=cwd)
    return dirpath


def is_windows():
    return sys.platform == 'win32'


def Popen(*args, **kwargs):
    """Drops the close_fds argument on Windows platforms in certain situations
    where it'd otherwise cause an exception from the subprocess module."""
    if is_windows() and 'close_fds' in kwargs:
        if 'stdin' in kwargs or 'stdout' in kwargs or 'stderr' in kwargs:
            kwargs.pop('close_fds')

    return subprocess.Popen(*args, **kwargs)


def drop_privileges(username):
    """
    Drops privileges to selected user.
    :param username: drop privileges to this username
    """
    if not HAVE_PWD:
        sys.exit(
            'Unable to import pwd required for dropping privileges (note that '
            'privilege dropping is not supported under Windows)!'
        )
