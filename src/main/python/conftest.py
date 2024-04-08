import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from main import app
import pytest
from config.database_config import db

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def init_db():
    """Initialize a clean database before each test."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db

@pytest.fixture(scope='session', autouse=True)
def teardown_db_after_file():
    """This fixture will be executed once after all test functions in the test file have run."""
    yield

    # Perform teardown actions here, such as cleaning up the database
    with app.app_context():
        db.drop_all()