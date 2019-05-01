import pytest

from aioworkers_orm.models import AIOWorkersModelMetaClass


@pytest.fixture
def config_yaml(db_url):
    return f"""
    db:
      cls: aioworkers_orm.databases.Database
      url: {db_url}
    models:
      cls: aioworkers_orm.models.Models
      models:
        first:
          module: app.models
          class_name: First
          table: sometable
          fields:
            id:
              type: integer
              primary_key: yes
      database: db
    """


@pytest.mark.sqlite
async def test_schema_models(context):
    assert AIOWorkersModelMetaClass.models
    assert 'app.models.First' in AIOWorkersModelMetaClass.models

    o = await context.models.first.objects.create(id=2)
    assert o
