import importlib
import pkgutil
import re
import sys

re_class_name = re.compile(r'([A-Z]*[a-z]*)')


def convert_class_name(name):
    """
    >>> convert_class_name('ClassName')
    'class_name'
    >>> convert_class_name('ABClassName')
    'abclass_name'
    """
    name_tokens = re_class_name.findall(name)
    return '_'.join(i.lower() for i in name_tokens if i)


def class_ref(cls: type):
    return cls.__module__ + '.' + cls.__name__


def import_modules(package, module=None):
    """
    Function import modules from tha package.
    """
    package = sys.modules[package]
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        if ispkg:
            try:
                m = '{}.{}.{}'.format(package.__name__, modname, module)
                importlib.import_module(m)
            except ImportError:
                pass
