import importlib
from typing import Type

import sqlalchemy
from aioworkers.core.base import AbstractConnector
from orm import Model

from aioworkers_orm.factory import ModelFactory
from aioworkers_orm.utils import convert_class_name, expand_class_ref


class Models(AbstractConnector):
    def __init__(self, config=None, *, context=None, loop=None):
        super().__init__(config, context=context, loop=loop)
        # Metadata used to create models from spec
        self._metadata = sqlalchemy.MetaData()
        self.database = None
        self._models = {}

    def set_config(self, config) -> None:
        super().set_config(config)

        # process models config node
        models_config = self.config.get("models", {})
        for name, model_spec in models_config.items():
            # add existed model class
            if isinstance(model_spec, str):
                # string means class reference
                module, cls_name = expand_class_ref(model_spec)
                m = importlib.import_module(module)
                model_cls = getattr(m, cls_name)
                self.add_model(model_cls, name=name)
            else:
                model_spec = dict(model_spec)
                model_cls = ModelFactory.create(model_spec, self._metadata)
                self.add_model(model_cls, name=name)

    def add_model(self, model_cls: Type[Model], name=None):
        name = name or convert_class_name(model_cls.__name__)
        # attach additional magic fields
        model_cls.__model_name__ = name
        model_cls.__context__ = self.context
        # Remember class
        self._models[name] = model_cls

    async def connect(self):
        self.database = self.context[self.config.database]
        for model_cls in self._models.values():
            model_cls.__database__ = self.database

    async def disconnect(self):
        for model_cls in self._models.values():
            self.remove_model(model_cls)

    @staticmethod
    def remove_model(model_cls: Type[Model]):
        if model_cls.__table__ is not None:
            model_cls.__context__ = None
            model_cls.__table__ = None
            model_cls.__database__ = None
            model_cls.__pkname__ = None
            model_cls.__model_name__ = None
            model_cls.__table__.metadata.remove(model_cls.__table__)

    def __getitem__(self, item: str):
        if hasattr(self, item):
            return getattr(self, item)
        return KeyError(item)

    def __getattr__(self, item: str):
        if item in self._models:
            model_cls = self._models[item]
            return model_cls
        raise AttributeError(f"{self} has no attribute {item}")

    def __iter__(self):
        return iter(self._models.values())
