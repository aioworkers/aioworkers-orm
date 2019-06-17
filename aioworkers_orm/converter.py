from orm import Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text, Time


class Converter:
    """
    Convert model spec to ORM model
    """
    types = {
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
    @classmethod
    def convert(cls, model_spec):
        from aioworkers_orm.models import AIOWorkersModelMetaClass, Model
        field_models = {}
        for k, v in model_spec['fields'].items():
            spec = dict(**v)
            t = spec.pop('type')
            field_cls = cls.types[t]
            field_models[k] = field_cls(**spec)
        c = AIOWorkersModelMetaClass.__new__(
            AIOWorkersModelMetaClass,
            model_spec['class_name'],
            (Model,), {
                '__module__': model_spec['module'],
                '__tablename__': model_spec['table'],
                **field_models,
            })

        return c
