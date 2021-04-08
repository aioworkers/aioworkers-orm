import pytest


@pytest.fixture
def config_yaml(db_dsn):
    return f"""
    db:
      cls: aioworkers_databases.database.Database
      dsn: {db_dsn}
    models:
      cls: aioworkers_orm.models.Models
      models:
        test: app.models.ModelTest
        first: app.first.models.ModelFirst
        second: app.second.models.ModelSecond
      database: db
    """


@pytest.mark.sqlite
async def test_context_models_list(context):
    o = await context.models.test.objects.create(id=2)
    assert o

    o = await context.models.test.objects.all()
    assert o

    o = await context.models.first.objects.create(id=1)
    assert o
    o = await context.models.first.get_by_id_sql(1)
    assert o

    o = await context.models.second.objects.create(id=1)
    assert o
    o = await context.models["second"].get_by_id(1)
    assert o

    with pytest.raises(KeyError):
        context.models["wrong_model"]

    with pytest.raises(AttributeError):
        context.models.wrong_model
