import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture(scope="session")
def client():
    with TestClient(app_module.app) as c:
        yield c


# Capture a snapshot of the initial in-memory activities so tests can restore state.
_initial_activities_snapshot = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Restore the activities dict before each test to ensure tests are isolated.
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_initial_activities_snapshot))
    yield
