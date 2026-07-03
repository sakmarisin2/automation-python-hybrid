import pytest

from src.api.services.automation_service import AutomationService


@pytest.fixture
def automation_service(base_config, session, base_headers):
    yield AutomationService(session=session, config=base_config, headers=base_headers)
