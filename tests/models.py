import orm
import sqlalchemy
from orm import NoMatch

from aioworkers_orm.models import Model


class Test(Model):
    __tablename__ = 'test'
    id = orm.Integer(primary_key=True)

    @classmethod
    async def get_by_id(cls, i):
        return await cls.objects.get(id=i)

    @classmethod
    async def get_by_id_sql(cls, i):
        sql = sqlalchemy.select([cls.__table__.c.id]).select_from(cls.__table__).where(
            cls.__table__.c.id == i
        )
        o = await cls.db.fetch_one(query=sql)
        if not o:
            raise NoMatch()
        return cls.from_row(o)
