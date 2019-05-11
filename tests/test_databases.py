import pytest


@pytest.fixture
def config_yaml(db_url):
    return f"""
    db:
      cls: aioworkers_orm.databases.Database
      dsn: {db_url}
    """


async def test_database(context):
    await context.db.execute('CREATE TABLE some_table (id INT);')
    await context.db.execute('DROP TABLE some_table;')
