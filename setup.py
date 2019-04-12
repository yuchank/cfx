import setuptools
import sys


def update_hashes():
    pass


# Provide hashes for our CWD migration process & update the $CWD/.cwd version.
# Only do these steps when "python setup.py sdist" is invoked.
if "setup.py" in sys.argv and "sdist" in sys.argv:
    update_hashes()
