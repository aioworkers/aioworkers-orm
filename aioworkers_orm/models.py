import typing

import orm
import sqlalchemy
from aioworkers.core.base import AbstractEntity
from orm.models import ModelMetaclass

from aioworkers_orm import utils


class AIOWorkersModelMetaClass(ModelMetaclass):
    metadata = sqlalchemy.MetaData()
    __models__ = {}

    def __new__(cls: type, name: str, bases: typing.Sequence[type], attrs: dict) -> type:
        attrs['__metadata__'] = AIOWorkersModelMetaClass.metadata
        ncls = super().__new__(cls, name, bases, attrs)
        name = utils.convert_class_name(name)
        AIOWorkersModelMetaClass.__models__[name] = ncls
        return ncls


class Model(orm.Model, metaclass=AIOWorkersModelMetaClass):
    __abstract__ = True


class Models(AbstractEntity):
    async def init(self):
        self.database = self.context[self.config.database]
        for i in AIOWorkersModelMetaClass.__models__.values():
            i.__database__ = self.database._db
            i.db = self.database._db
            i.context = self.context

    @property
    def metadata(self):
        return AIOWorkersModelMetaClass.metadata

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        return KeyError(item)

    def __getattr__(self, item):
        if item in AIOWorkersModelMetaClass.__models__:
            model_cls = AIOWorkersModelMetaClass.__models__[item]
            return model_cls
        raise AttributeError('%r has no attribute %r' % (self, item))
