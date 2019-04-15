import re

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
