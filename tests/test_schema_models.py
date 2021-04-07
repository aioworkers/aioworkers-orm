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
        first:
          module: app.models
          name: First
          table: sometable
          fields:
            id:
              type: integer
              primary_key: yes
      database: db
    """


@pytest.mark.sqlite
async def test_schema_models(context):
    o = await context.models.first.objects.create(id=2)
    assert o
