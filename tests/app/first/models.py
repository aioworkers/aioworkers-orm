import orm
import sqlalchemy
from orm import NoMatch

from aioworkers_orm.models import Model


class ModelFirst(Model):
    __tablename__ = 'model_first'
    id = orm.Integer(primary_key=True)

    @classmethod
    async def get_by_id_sql(cls, i):
        t = cls.objects.table
        sql = sqlalchemy.select([t.c.id]).select_from(t).where(t.c.id == i)
        o = await cls.objects.database.fetch_one(query=sql)
        if not o:
            raise NoMatch()
        return cls.from_row(o)
