from cfx.core.plugins import enumerate_plugins
from cfx.common.abstracts import Machinery

plugins = enumerate_plugins(__file__, 'cfx.machinery', globals(), Machinery, as_dict=True)