import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest
from playwright.sync_api import sync_playwright
from api_client import QiwiApiClient

@pytest.fixture(scope="session")
def api_request_context():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        yield request_context
        request_context.dispose()

@pytest.fixture(scope="session")
def api_client(api_request_context):
    base_url = os.getenv("QIWI_BASE_URL", "https://api.qiwi.com/partner/payout")
    token = os.getenv("QIWI_TOKEN", "mock-token-123456")
    agent_id = os.getenv("QIWI_AGENT_ID", "12345")
    point_id = os.getenv("QIWI_POINT_ID", "67890")
    
    return QiwiApiClient(
        request_context=api_request_context,
        base_url=base_url,
        token=token,
        agent_id=agent_id,
        point_id=point_id
    )
