import re

re_class_name = re.compile(r"([A-Z]*[a-z]*)")


def convert_class_name(name):
    """
    >>> convert_class_name('ClassName')
    'class_name'
    >>> convert_class_name('ABClassName')
    'abclass_name'
    """
    name_tokens = re_class_name.findall(name)
    return "_".join(i.lower() for i in name_tokens if i)


def class_ref(cls: type):
    """
    >>> class_ref(int)
    'builtins.int'
    """
    return cls.__module__ + "." + cls.__name__


def expand_class_ref(cls_ref: str):
    """
    >>> expand_class_ref('test.test.Test')
    ('test.test', 'Test')
    """
    parts = cls_ref.rpartition(".")
    return parts[0], parts[-1]
