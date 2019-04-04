import subprocess
import sys


def is_windows():
    return sys.platform == 'win32'


def Popen(*args, **kwargs):
    """Drops the close_fds argument on Windows platforms in certain situations
    where it'd otherwise cause an exception from the subprocess module."""
    if is_windows() and 'close_fds' in kwargs:
        if 'stdin' in kwargs or 'stdout' in kwargs or 'stderr' in kwargs:
            kwargs.pop('close_fds')

    return subprocess.Popen(*args, **kwargs)
