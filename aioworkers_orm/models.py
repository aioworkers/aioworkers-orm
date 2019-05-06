import orm
import sqlalchemy
from aioworkers.core.base import AbstractConnector
from aioworkers.core.context import Context
from orm.fields import (Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text,
                        Time)
from orm.models import ModelMetaclass

from aioworkers_orm.utils import class_ref, convert_class_name

TYPES_MAP = {
    'boolean': Boolean,
    'integer': Integer,
    'float': Float,
    'string': String,
    'text': Text,
    'date': Date,
    'time': Time,
    'datetime': DateTime,
    'json': JSON,
    'foreignkey': ForeignKey,
}


class AIOWorkersModelMetaClass(ModelMetaclass):
    __models__ = {}

    def __new__(mcls, name, bases, attrs) -> type:
        cls = super(ModelMetaclass, mcls).__new__(mcls, name, bases, attrs)

        if attrs.get('__abstract__'):
            return cls

        model_id = class_ref(cls)
        cls.__model_id__ = model_id
        AIOWorkersModelMetaClass.__models__[model_id] = cls

        return cls


class Model(orm.Model, metaclass=AIOWorkersModelMetaClass):
    __abstract__ = True
    __context__ = None  # type: Context
    __model_id__ = None  # type: str
    __model_name__ = None  # type: str

    @property
    def context(self):
        return self.__context__


class Models(AbstractConnector):
    def __init__(self, config=None, *, context=None, loop=None):
        super().__init__(config, context=context, loop=loop)
        self.database = None
        self.metadata = sqlalchemy.MetaData()
        self.__models = {}

    @staticmethod
    def create_model(table, module, class_name, fields):
        # Convert fields descriptions to ORM Fields
        field_models = {}
        for k, v in fields.items():
            spec = dict(**v)
            t = spec.pop('type')
            cls = TYPES_MAP[t]
            field_models[k] = cls(**spec)
        c = AIOWorkersModelMetaClass.__new__(AIOWorkersModelMetaClass, class_name, (Model,), {
            '__module__': module,
            '__tablename__': table,
            **field_models,
        })
        return class_ref(c)

    async def connect(self):
        self.database = self.context[self.config.database]

        models_list = self.config.get('models', {})
        if models_list:
            for name, model_spec in models_list.items():
                if isinstance(model_spec, str):
                    # specified just model id
                    self.add_model(model_spec, name=name)
                elif 'table' in model_spec:
                    # specified custom model
                    model_id = self.create_model(**model_spec)
                    self.add_model(model_id, name)
        else:
            # Iterate over all the models
            filter_config = self.config.get('filter', {})
            package_filter = filter_config.get('package')
            package_filter = package_filter + '.' if package_filter else package_filter
            module_filter = filter_config.get('module')
            for model_id in AIOWorkersModelMetaClass.__models__:
                *_, m, _ = model_id.split('.')
                if package_filter and not model_id.startswith(package_filter):
                    continue
                if module_filter and m != module_filter:
                    continue
                self.add_model(model_id)

    async def disconnect(self):
        for model_cls in self.__models.values():
            self.remove_model(model_cls)

    def add_model(self, model_id, name=None):
        cls = AIOWorkersModelMetaClass.__models__[model_id]
        if hasattr(cls, '__table__') and cls.__table__ is not None:
            raise ValueError('Model already bind to another metadata.')
        if not name:
            name = convert_class_name(cls.__name__)
        cls.__database__ = self.database.db
        cls.__context__ = self.context

        pkname = None

        columns = []
        for field_name, field in cls.fields.items():
            if field.primary_key:
                pkname = field_name
            columns.append(field.get_column(field_name))

        cls.__table__ = sqlalchemy.Table(cls.__tablename__, self.metadata, *columns)
        cls.__pkname__ = pkname

        self.__models[name] = cls
        cls.__model_name__ = name

    def remove_model(self, model_cls):
        if model_cls.__table__ is not None:
            self.metadata.remove(model_cls.__table__)
            model_cls.__context__ = None
            model_cls.__table__ = None
            model_cls.__database__ = None
            model_cls.__pkname__ = None
            model_cls.__model_name__ = None

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        return KeyError(item)

    def __getattr__(self, item):
        if item in self.__models:
            model_cls = self.__models[item]
            return model_cls
        raise AttributeError('%r has no attribute %r' % (self, item))
