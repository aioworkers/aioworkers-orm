import pytest


@pytest.fixture
def config_yaml(db_url):
    return f"""
    db:
      cls: aioworkers_orm.databases.Database
      dsn: {db_url}
    models:
      cls: aioworkers_orm.models.Models
      models:
        first: tests.app.first.models.ModelFirst
      database: db
    """


@pytest.mark.sqlite
async def test_context_models_list(context):
    o = await context.models.first.objects.create(id=2)
    assert o
