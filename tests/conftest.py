import pathlib

import pytest
import sqlalchemy


@pytest.fixture(scope="session")
def db_name():
    return "test.db.sqlite"


@pytest.fixture(scope="session")
def db_dsn(db_name):
    return f"sqlite:///{db_name}"


@pytest.fixture(autouse=True)
def _sqlite_marker(request):
    marker = request.node.get_closest_marker("sqlite")
    if marker:
        request.getfixturevalue("sqlite_setup")


@pytest.fixture
def sqlite_setup(context, db_dsn, db_name):
    # Delete sqlite db file from previous run
    p = pathlib.Path(__file__).parent.with_name(db_name)
    if p.exists():
        p.unlink()

    # Create tables for test purposes for entities which name starts from "models"
    engine = sqlalchemy.create_engine(db_dsn)
    for i in dir(context):
        if i.startswith("models"):
            for model in context[i]:
                model.__table__.metadata.create_all(engine)
