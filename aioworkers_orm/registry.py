from aioworkers_orm.utils import class_ref


class ModelsRegistry:
    """
    Global registry for all ORM models.
    """

    __models__ = {}

    @classmethod
    def add_model(cls, model_cls):
        from aioworkers_orm.models import Model

        if not issubclass(model_cls, Model):
            raise ValueError("Model have to be subclass of aioworkers_orm.models.Model")

        model_id = cls.get_model_id(model_cls)
        if model_id in cls.__models__ or model_cls.__model_id__ is not None:
            raise ValueError(f"{model_id} already in registry")
        model_cls.__model_id__ = model_id
        cls.__models__[model_id] = model_cls

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

    @classmethod
    def get_model_id(cls, model_cls):
        return class_ref(model_cls)
