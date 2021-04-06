import orm

from aioworkers_orm.models import Model


class ModelTest(Model):
    __tablename__ = "model_test"
    id = orm.Integer(primary_key=True)
