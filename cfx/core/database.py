from cfx.common.config import config

from cfx.common.utils import Singleton

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Database(object):
    """Analysis queue database.

    This class handles the creation of the database user for internal queue
    management. It also provides some functions for interacting with it.
    """
    __metaclass__ = Singleton

    def __init__(self, schema_check=True, echo=False):
        """
        :param schema_check: disable or enable the db schema version check.
        :param echo: echo sql queries.
        """
        self._lock = None

    def connect(self, schema_check=None, dsn=None, create=True):
        """Connect to the database backend."""
        if not dsn:
            dsn = config('cfx:database:connection')
        if not dsn:
            dsn = 'sqlite:///%s' % cwd('cuckoo.db')

        self._connect_database(dsn)

    def _connect_database(self, connection_string):
        """
        Connect to a Database.
        :param connection_string: Connection string specifying the database
        :return:
        """
        self.engine = create_engine(connection_string)

    def view_task(self, task_id, details=True):
        """Retrieve information on a task.
        @param task_id: ID of the task to query.
        @return: details on the task.
        """
