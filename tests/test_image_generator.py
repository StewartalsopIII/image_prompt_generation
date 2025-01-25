"""
Tests for image generation functionality with error handling.
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch
import replicate
import requests

from image_generation.image_generator import ImageGenerator, APIError

@pytest.fixture
def image_generator():
    """Fixture for ImageGenerator instance with mocked configuration."""
    with patch('image_generation.image_generator.load_config') as mock_config:
        mock_config.return_value = {
            'api_token': 'test_token',
            'output_dir': tempfile.mkdtemp()
        }
        generator = ImageGenerator(max_retries=2, base_delay=0.1)
        yield generator

def test_init_with_custom_params():
    """Test ImageGenerator initialization with custom parameters."""
    generator = ImageGenerator(max_retries=5, base_delay=2.0)
    assert generator.max_retries == 5
    assert generator.base_delay == 2.0

def test_handle_api_error_rate_limit():
    """Test handling of rate limit errors."""
    generator = ImageGenerator()
    error = replicate.exceptions.ReplicateError("Rate limit exceeded")
    should_retry, message = generator._handle_api_error(error)
    assert should_retry == True
    assert "Rate limit" in message

def test_handle_api_error_invalid_token():
    """Test handling of invalid API token."""
    generator = ImageGenerator()
    error = replicate.exceptions.ReplicateError("Unauthorized access")
    should_retry, message = generator._handle_api_error(error)
    assert should_retry == False
    assert "Invalid API token" in message

def test_handle_api_error_network():
    """Test handling of network errors."""
    generator = ImageGenerator()
    error = requests.exceptions.ConnectionError("Connection failed")
    should_retry, message = generator._handle_api_error(error)
    assert should_retry == True
    assert "Network error" in message

@patch('time.sleep')  # Prevent actual sleeping in tests
def test_generate_image_retry_success(mock_sleep, image_generator):
    """Test successful image generation after retry."""
    with patch.object(image_generator.client, 'run') as mock_run:
        # Fail first, succeed on retry
        mock_run.side_effect = [
            replicate.exceptions.ReplicateError("Rate limit exceeded"),
            ["http://example.com/image.png"]
        ]
        
        with patch('image_generation.image_generator.save_image_from_url') as mock_save:
            mock_save.return_value = "/path/to/saved/image.png"
            
            result = image_generator.generate_image("test prompt")
            
            assert result['filepath'] == "/path/to/saved/image.png"
            assert result['prompt'] == "test prompt"
            assert mock_run.call_count == 2
            mock_sleep.assert_called_once()

@patch('time.sleep')
def test_generate_image_max_retries_exceeded(mock_sleep, image_generator):
    """Test failure after maximum retries."""
    with patch.object(image_generator.client, 'run') as mock_run:
        mock_run.side_effect = replicate.exceptions.ReplicateError("Rate limit exceeded")
        
        with pytest.raises(APIError) as exc_info:
            image_generator.generate_image("test prompt")
        
        assert "Rate limit" in str(exc_info.value)
        assert mock_run.call_count == 3  # Initial try + 2 retries
        assert mock_sleep.call_count == 2

def test_generate_image_invalid_prompt(image_generator):
    """Test handling of invalid prompts."""
    with pytest.raises(ValueError) as exc_info:
        image_generator.generate_image("")
    assert "empty" in str(exc_info.value).lower()

    with pytest.raises(ValueError) as exc_info:
        image_generator.generate_image("   ")
    assert "empty" in str(exc_info.value).lower()

@patch('time.sleep')
def test_generate_image_unretryable_error(mock_sleep, image_generator):
    """Test handling of unretryable errors."""
    with patch.object(image_generator.client, 'run') as mock_run:
        mock_run.side_effect = replicate.exceptions.ModelError("Invalid model")
        
        with pytest.raises(APIError) as exc_info:
            image_generator.generate_image("test prompt")
        
        assert "Model error" in str(exc_info.value)
        assert mock_run.call_count == 1  # Should not retry
        assert mock_sleep.call_count == 0

def test_generate_image_unexpected_error(image_generator):
    """Test handling of unexpected errors."""
    with patch.object(image_generator.client, 'run') as mock_run:
        mock_run.side_effect = Exception("Unexpected error")
        
        with pytest.raises(APIError) as exc_info:
            image_generator.generate_image("test prompt")
        
        assert "Unexpected error" in str(exc_info.value)