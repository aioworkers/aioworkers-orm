import orm
from .meta import metadata


class ModelTest(orm.Model):
    __tablename__ = "model_test"
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)
