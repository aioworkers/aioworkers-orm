import orm
import sqlalchemy
from aioworkers.core.base import AbstractConnector
from aioworkers.core.context import Context
from orm.models import ModelMetaclass

from aioworkers_orm.registry import ModelsRegistry
from aioworkers_orm.utils import convert_class_name


class AIOWorkersModelMetaClass(ModelMetaclass):
    def __new__(mcls, name, bases, attrs) -> type:
        cls = super(ModelMetaclass, mcls).__new__(mcls, name, bases, attrs)

        if attrs.get('__abstract__'):
            return cls
        # Register all models
        ModelsRegistry.add_model(cls)

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
        self._models = {}
        self._ids = set()
        self._custom_names = {}

    async def init(self):
        self.create_models()
        self.search_models()
        self.filter_models()

    def create_models(self):
        """
        Get models specs and create dynamic models in registry
        """
        for name, model_spec in self.config.get('models', {}).items():
            if 'table' in model_spec:
                model_id = ModelsRegistry.create_model(**model_spec)
                # Model spec which defined in models entity have to be bind to it.
                self._ids.add(model_id)

    def search_models(self):
        """
        Search models which can be bind.
        """
        models_config = self.config.get('models', {})
        if not models_config:
            # All models can be potentially bind to entity
            self._ids.update(ModelsRegistry.ids())
            return

        for name, model_spec in models_config.items():
            if isinstance(model_spec, str):
                self._ids.add(model_spec)
                self._custom_names[model_spec] = name

    def filter_models(self):
        """
        Filter models according config
        """
        # Iterate over all the models
        filter_config = self.config.get('filter', {})
        package_filter = filter_config.get('package')
        package_filter = package_filter + '.' if package_filter else package_filter
        module_filter = filter_config.get('module')
        for model_id in set(self._ids):
            *_, m, _ = model_id.split('.')
            if package_filter and not model_id.startswith(package_filter):
                self._ids.remove(model_id)
            if module_filter and m != module_filter:
                self._ids.remove(model_id)

    def bind_models(self):
        """
        Bind models to the models entity.
        """
        for model_id in self._ids:
            name = self._custom_names.get(model_id)
            self.bind_model(model_id, name=name)

    async def connect(self):
        self.database = self.context[self.config.database]
        self.bind_models()

    async def disconnect(self):
        for model_cls in self._models.values():
            self.remove_model(model_cls)

    def bind_model(self, model_id, name=None):
        cls = ModelsRegistry.get_model(model_id)
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

        self._models[name] = cls
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
        if item in self._models:
            model_cls = self._models[item]
            return model_cls
        raise AttributeError('%r has no attribute %r' % (self, item))
