import orm

from aioworkers_orm.models import Model


class ModelSecond(Model):
    __tablename__ = 'model_second'
    id = orm.Integer(primary_key=True)

    @classmethod
    async def get_by_id(cls, i):
        return await cls.objects.get(id=i)
