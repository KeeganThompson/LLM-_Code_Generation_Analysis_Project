import pytest
import json
import sys

GLOBAL_TEST_RESULTS = {"time_ms": 0.0} 

def pytest_addoption(parser):
    parser.addoption(
        "--model-path", action="store", default=None, help="Path to the generated SplayTree file to test."
    )

@pytest.fixture
def module_path(request):
    return request.config.getoption("--model-path")

def pytest_sessionfinish(session):
    print(json.dumps(GLOBAL_TEST_RESULTS), file=sys.stdout)