import pytest

from aioworkers_orm.registry import ModelsRegistry


def test_wrong_model_id():
    with pytest.raises(ValueError):
        ModelsRegistry.get_model('not_existed_model')


def test_model_list():
    ids = list(ModelsRegistry.ids())
    assert ids == [
        'tests.app.models.ModelTest',
        'tests.app.first.models.ModelFirst',
        'tests.app.second.models.ModelSecond',
    ]


def test_add_model():
    from tests.app.models import ModelTest
    with pytest.raises(ValueError):
        ModelsRegistry.add_model(ModelTest)
