import pytest

from aioworkers_orm.registry import ModelsRegistry


def test_not_existed_model():
    with pytest.raises(AttributeError):
        ModelsRegistry.get_model('not_existed_model')
