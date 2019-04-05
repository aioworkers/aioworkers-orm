import pathlib

import pytest
import sqlalchemy


@pytest.fixture(scope='session')
def db_name():
    return 'test.db.sqlite'


@pytest.fixture(scope='session')
def db_url(db_name):
    return f"sqlite:///{db_name}"


@pytest.fixture(scope="session", autouse=True)
def cleanup(request, db_name, db_url):
    # Delete sqlite db file from previous run
    p = pathlib.Path(__file__).parent.with_name(db_name)
    if p.exists():
        p.unlink()

    from aioworkers_orm.models import AIOWorkersModelMetaClass
    engine = sqlalchemy.create_engine(db_url)
    AIOWorkersModelMetaClass.metadata.create_all(engine)


@pytest.fixture
def config_yaml(db_url):
    return f"""
    db:
      cls: aioworkers_orm.databases.Database
      url: {db_url}
    models:
      cls: aioworkers_orm.models.Models
      database: db
    """
