
class Type(object):
    """Base Class for Type Definitions"""
    def __init__(self, default=None, required=True, sanitize=False, allow_empty=False):
        self.sanitize = sanitize


class Int(Type):
    """Integer Type Definition class."""
    pass


class String(Type):
    """String Type Definition class."""
    pass


class Config(object):
    """Configuration file parser."""

    configuration = {
        'cfx': {
            'database': {
                'connection': String(sanitize=True),
                'timeout': Int(60, allow_empty=True)
            },
        },
    }

    def __init__(self, file_name='cfx', cfg=None, strict=False, loose=False, raw=False):
        """
        :param file_name: file name without extension.
        :param cfg: configuration file path.
        :param strict:
        :param loose:
        :param raw:
        """
        env = {}


def config(s, cfg=None, strict=False, raw=False, loose=False, check=False):
    """Fetch a configuration value, denoted as file:section:key."""
    if s.count(':') != 2:
        raise RuntimeError('Invalid configuration entry: %s' % s)

    file_name, section, key = s.split(':')

    if check:
        strict = raw = loose = True

    type_ = Config.configuration.get(file_name, {}).get(section, {}).get(key)
    print(type_)
