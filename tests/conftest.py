import pytest


@pytest.fixture
def config_yaml():
    return """
    models:
      cls: aioworkers_orm.models.Models
    """
