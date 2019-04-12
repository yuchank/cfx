import logging
import threading

from cfx.common.config import config
from cfx.common.exceptions import CFXDependencyError
from cfx.common.utils import Singleton, classlock
from cfx.misc import cwd

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

log = logging.getLogger(__name__)


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
            dsn = config("cfx:database:connection")
        if not dsn:
            dsn = "sqlite:///%s" % cwd("cuckoo.db")

        database_flavor = dsn.split(":", 1)[0].lower()
        if database_flavor == "sqlite":
            log.debug("Using database-wide lock for sqlite")
            self._lock = threading.RLock()

        self._connect_database(dsn)

        # Connection timeout.
        self.engine.pool_timeout = config("cfx:database:timeout")

        # Get db session.
        self.Session = sessionmaker(bind=self.engine)

        if create:
            self._create_tables()

    def _create_tables(self):
        """
        Creates all the database tables etc.
        """

    def _connect_database(self, connection_string):
        """
        Connect to a Database.
        :param connection_string: Connection string specifying the database
        :return:
        """
        try:
            if connection_string.startswith("sqlite"):
                # Using "check_same_thread" to disable sqlite safety check on multiple threads.
                self.engine = create_engine(connection_string, connect_args={"check_same_thread": False})
            else:
                self.engine = create_engine(connection_string)
        except ImportError as e:
            lib = e.message.split()[-1]
            if lib == "MySQLdb":
                raise CFXDependencyError(
                    "Missing MySQL database driver (install with "
                    "`pip install mysql-python` on Linux or `pip install "
                    "mysqlclient` on Windows"
                )

            raise CFXDependencyError(
                "Missing unknown database driver, unable to import %s" % lib
            )

    def view_task(self, task_id, details=True):
        """Retrieve information on a task.
        @param task_id: ID of the task to query.
        @return: details on the task.
        """

    @classlock
    def get_available_machines(self):
        """
        Which machines are available
        :return: free virtual machines
        """
        session = self.Session
