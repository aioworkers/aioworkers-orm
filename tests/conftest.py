import pathlib

import pytest
import sqlalchemy


@pytest.fixture(scope='session')
def db_name():
    return 'test.db.sqlite'


@pytest.fixture(scope='session')
def db_url(db_name):
    return f"sqlite:///{db_name}"


@pytest.fixture(autouse=True)
def _sqlite_marker(request):
    """Implement the mongo_db marker.
    """
    marker = request.node.get_closest_marker('sqlite')
    if marker:
        request.getfixturevalue('sqlite_setup')


@pytest.fixture
def sqlite_setup(context, db_url, db_name):
    # Delete sqlite db file from previous run
    p = pathlib.Path(__file__).parent.with_name(db_name)
    if p.exists():
        p.unlink()

    engine = sqlalchemy.create_engine(db_url)
    for i in dir(context):
        if i.startswith('models'):
            context[i].metadata.create_all(engine)
