import os
import importlib

from cfx.common.exceptions import (CFXOperationalError)


def enumerate_plugins(dirpath, module_prefix, namespace, class_, attributes={}, as_dict=False):
    """Import plugins of type 'class' located at 'dirpath' into the 'namespace' that starts with 'module_prefix'.
    If 'dirpath' represents a filepath then it is converted into its containing directory.
    The 'attributes' dictionary allows one to set extra fields for all imported plugins.
    Using 'as_dict' a dictionary based on the module name is returned."""
    if os.path.isfile(dirpath):
        dirpath = os.path.dirname(dirpath)

    for fname in os.listdir(dirpath):
        if fname.endswith('.py') and not fname.startswith('__init__'):
            module_name, _ = os.path.splitext(fname)
            try:
                importlib.import_module('%s.%s' % (module_prefix, module_name))
            except ImportError as e:
                raise CFXOperationalError(
                    'Unable to load the cfx plugin at %s.%s. Please '
                    'review its contents and/or validity~' % (fname, e)
                )

    subclasses = class_.__subclasses__()[:]

    plugins = []
    while subclasses:
        subclass = subclasses.pop(0)

        # Include subclasses of this subclass (there are some subclasses, e.g.,
        # LibVirtMachinery, that fail the following module namespace
        # check and as such we perform this logic here).
        subclasses.extend(subclass.__subclasses__())

        # Check whether this subclass belongs to the module namespace that
        # we're currently importing. It should be noted that parent and child
        # namespace should fail the following if-statement.
        if module_prefix != '.'.join(subclass.__module__.split('.')[:-1]):
            continue

        namespace[subclass.__name__] = subclass
        for key, value in attributes.items():
            setattr(subclass, key, value)

        plugins.append(subclass)

    if as_dict:
        ret = {}
        for plugin in plugins:
            ret[plugin.__module__.split('.')[-1]] = plugin
        return ret

    return sorted(plugins, key=lambda x: x.__name__.lower())
