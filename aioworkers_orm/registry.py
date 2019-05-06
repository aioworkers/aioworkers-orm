from orm import Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text, Time

from aioworkers_orm.utils import class_ref

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


class ModelsRegistry:
    """
    Global registry for all ORM models.
    """
    __models__ = {}

    @classmethod
    def add_model(cls, model_cls):
        model_id = class_ref(model_cls)
        if model_id in cls.__models__ or model_cls.__model_id__ is not None:
            raise ValueError(f"{model_id} already in registry")
        model_cls.__model_id__ = model_id
        cls.__models__[model_id] = model_cls

    @classmethod
    def create_model(cls, table, module, class_name, fields):
        from aioworkers_orm.models import AIOWorkersModelMetaClass, Model
        # Convert fields descriptions to ORM Fields
        field_models = {}
        for k, v in fields.items():
            spec = dict(**v)
            t = spec.pop('type')
            field_cls = TYPES_MAP[t]
            field_models[k] = field_cls(**spec)
        c = AIOWorkersModelMetaClass.__new__(AIOWorkersModelMetaClass, class_name, (Model,), {
            '__module__': module,
            '__tablename__': table,
            **field_models,
        })
        return class_ref(c)

    @classmethod
    def get_model(cls, model_id):
        if model_id in cls.__models__:
            model_cls = cls.__models__[model_id]
            return model_cls
        raise ValueError(f"Model {model_id} does not exist...")

    @classmethod
    def models(cls):
        return cls.__models__.values()

    @classmethod
    def ids(cls):
        return cls.__models__.keys()
