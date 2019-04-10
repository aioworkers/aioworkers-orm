import databases
from aioworkers.core.base import AbstractConnector


class Database(AbstractConnector):
    """
    Use Wrapper (Decorator) pattern to wrap Database and add it behavior to entity.
    """

    __bind_methods = (
        'execute',
        'execute_many',
        'fetch_all',
        'fetch_val',
        'fetch_one',
        'iterate',
        'transaction',
        'connection',
    )

    def __init__(self, config=None, *, context=None, loop=None):
        super().__init__(config, context=context, loop=loop)
        self.db = databases.Database(self.config.url)
        for method_name in self.__bind_methods:
            f = getattr(self.db, method_name)
            if f:
                setattr(self, method_name, f)

    async def connect(self):
        await self.db.connect()

    async def disconnect(self):
        await self.db.disconnect()
