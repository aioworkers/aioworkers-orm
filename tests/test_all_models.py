import pytest


@pytest.fixture
def config_yaml(db_dsn):
    return f"""
    db:
      cls: aioworkers_databases.database.Database
      dsn: {db_dsn}
    models:
      cls: aioworkers_orm.models.Models
      database: db
    logging:
      version: 1
      disable_existing_loggers: false
      root:
        level: DEBUG
        handlers: [console]
      handlers:
        console:
          level: ERROR
          class: logging.StreamHandler
      loggers:
        aioworkers_databases:
          level: DEBUG
          handlers: [console]
          propagate: true
    """


@pytest.mark.sqlite
async def test_context_all_models(context):
    o = await context.models.model_first.objects.create(id=1)
    assert o
    o = await context.models.model_first.get_by_id_sql(1)
    assert o

    o = await context.models.model_second.objects.create(id=1)
    assert o
    o = await context.models.model_second.get_by_id(1)
    assert o


@pytest.mark.sqlite
async def test_orm(context):
    from tests.app.first.models import ModelFirst

    o = await ModelFirst.objects.create(id=1)
    assert o
