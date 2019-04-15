import pytest


@pytest.fixture
def config_yaml(db_url):
    return f"""
    db:
      cls: aioworkers_orm.databases.Database
      url: {db_url}
    models:
      cls: aioworkers_orm.models.Models
      database: db
      filter:
        package: tests.app.second
        module: models
    """


@pytest.mark.sqlite
async def test_models_search(context):
    o = await context.models.model_second.objects.create(id=1)
    assert o
