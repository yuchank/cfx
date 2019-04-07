from cfx.common.utils import Singleton

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Database(object):
    """Analysis queue database.

    This class handles the creation of the database user for internal queue
    management. It also provides some functions for interacting with it.
    """
    __metaclass__ = Singleton
