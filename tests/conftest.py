"""
Shared test configuration and fixtures.
"""

import pytest
import os
import tempfile
import shutil
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Automatically mock environment variables for all tests."""
    with patch.dict(os.environ, {
        'REPLICATE_API_TOKEN': 'test_token'
    }):
        yield

@pytest.fixture
def temp_test_dir():
    """Create a temporary directory for test files."""
    test_dir = tempfile.mkdtemp()
    yield test_dir
    shutil.rmtree(test_dir)

@pytest.fixture
def mock_successful_api():
    """Mock successful API response."""
    with patch('replicate.Client.run') as mock_run:
        mock_run.return_value = ["http://example.com/test_image.png"]
        yield mock_run

@pytest.fixture
def mock_failed_api():
    """Mock failed API response."""
    with patch('replicate.Client.run') as mock_run:
        mock_run.side_effect = Exception("API Error")
        yield mock_run