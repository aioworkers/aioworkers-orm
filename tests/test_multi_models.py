import pytest


@pytest.fixture
def config_yaml(db_url):
    return f"""
    db:
      cls: aioworkers_orm.databases.Database
      dsn: {db_url}
    models_first:
      cls: aioworkers_orm.models.Models
      database: db
      filter:
        package: tests.app.first
        module: models
    models_second:
      cls: aioworkers_orm.models.Models
      database: db
      filter:
        package: tests.app.second
        module: models
    """


@pytest.mark.sqlite
async def test_models(context):
    o = await context.models_first.model_first.objects.create(id=1)
    assert o

    o = await context.models_second.model_second.objects.create(id=1)
    assert o
