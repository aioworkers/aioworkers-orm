import orm
from ..meta import metadata


class ModelSecond(orm.Model):
    __tablename__ = "model_second"
    __metadata__ = metadata
    id = orm.Integer(primary_key=True)

    @classmethod
    async def get_by_id(cls, i):
        return await cls.objects.get(id=i)
