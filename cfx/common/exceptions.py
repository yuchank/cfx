class CFXCriticalError(Exception):
    """
    CFX struggle in a critical error.
    """


class CFXStartupError(CFXCriticalError):
    """
    Error starting up CFX.
    """


class CFXOperationalError(Exception):
    """
    CFX operational error.
    """
