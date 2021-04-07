from typing import Type
from orm import Model
from orm.models import ModelMetaclass

from orm import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    Time,
)
from sqlalchemy import MetaData


class ModelFactory:
    """
    Create ORM model by specification
    """

    types = {
        "boolean": Boolean,
        "integer": Integer,
        "float": Float,
        "string": String,
        "text": Text,
        "date": Date,
        "time": Time,
        "datetime": DateTime,
        "json": JSON,
        "foreignkey": ForeignKey,
    }

    @classmethod
    def create(cls, model_spec: dict, metadata: MetaData) -> Type[Model]:
        fields = {}
        for k, v in model_spec["fields"].items():
            spec = dict(**v)
            t = spec.pop("type")
            field_cls = cls.types[t]
            fields[k] = field_cls(**spec)

        model_cls = ModelMetaclass.__new__(
            ModelMetaclass,
            model_spec["name"],
            (Model,),
            {
                "__module__": model_spec.get("module"),
                "__tablename__": model_spec["table"],
                "__metadata__": metadata,
                **fields,
            },
        )

        return model_cls
