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
        for field_name, field_spec in model_spec["fields"].items():
            field_spec = dict(field_spec)
            field_type = field_spec.pop("type")
            field_cls = cls.types[field_type]
            fields[field_name] = field_cls(**field_spec)

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
