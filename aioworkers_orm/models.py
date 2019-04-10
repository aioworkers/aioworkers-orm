import orm
import sqlalchemy
from aioworkers.core.base import AbstractEntity
from orm.models import ModelMetaclass

from aioworkers_orm.utils import class_ref, convert_class_name


class AIOWorkersModelMetaClass(ModelMetaclass):
    models = {}

    def __new__(mcls, name, bases, attrs) -> type:
        cls = super(ModelMetaclass, mcls).__new__(mcls, name, bases, attrs)

        if attrs.get('__abstract__'):
            return cls

        model_id = class_ref(cls)
        AIOWorkersModelMetaClass.models[model_id] = cls

        return cls


class Model(orm.Model, metaclass=AIOWorkersModelMetaClass):
    __abstract__ = True
    __context__ = None

    @property
    def context(self):
        return self.__context__


class Models(AbstractEntity):
    def __init__(self, config=None, *, context=None, loop=None):
        super().__init__(config, context=context, loop=loop)
        self.database = None
        self.metadata = sqlalchemy.MetaData()
        self.__models = {}

    async def init(self):
        self.database = self.context[self.config.database]

        # import_config = self.config.get('import', {})
        # if import_config:
        #     import_modules(import_config.package, import_config.module)

        models_list = self.config.get('models', {})
        if models_list:
            for name, model_id in models_list.items():
                self.add_model(model_id, name)
        else:
            # Iterate over all the models
            filter_config = self.config.get('filter', {})
            package_filter = filter_config.get('package')
            package_filter = package_filter + '.' if package_filter else package_filter
            module_filter = filter_config.get('module')
            for model_id in AIOWorkersModelMetaClass.models.keys():
                *_, m, _ = model_id.split('.')
                if package_filter and not model_id.startswith(package_filter):
                    continue
                if module_filter and m != module_filter:
                    continue
                self.add_model(model_id)

    def add_model(self, model_id, name=None):
        cls = AIOWorkersModelMetaClass.models[model_id]
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

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        return KeyError(item)

    def __getattr__(self, item):
        if item in self.__models:
            model_cls = self.__models[item]
            return model_cls
        raise AttributeError('%r has no attribute %r' % (self, item))
