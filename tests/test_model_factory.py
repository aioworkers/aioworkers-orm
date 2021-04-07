import sqlalchemy

from aioworkers_orm.factory import ModelFactory


async def test_create_model():
    metadata = sqlalchemy.MetaData()
    model_cls = ModelFactory.create(
        {
            "name": "First",
            "module": "app.models",
            "table": "sometable",
            "fields": {"id": {"type": "integer", "primary_key": True}},
        },
        metadata,
    )
    assert model_cls.__module__ == "app.models"
    assert model_cls.__name__ == "First"
