"""
Tests for utility functions with enhanced error handling.
"""

import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, mock_open
from PIL import Image
import requests
from io import BytesIO

from image_generation.utils import (
    check_disk_space,
    validate_image,
    create_backup,
    save_image_from_url,
    validate_prompt,
    ImageSaveError
)

@pytest.fixture
def temp_dir():
    """Fixture for temporary directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_image():
    """Fixture for a sample PIL Image."""
    img = Image.new('RGB', (100, 100), color='red')
    return img

def test_check_disk_space(temp_dir):
    """Test disk space checking functionality."""
    # Test with small required space
    assert check_disk_space(temp_dir, 1024) == True
    
    # Test with extremely large required space
    huge_space = 1024 * 1024 * 1024 * 1024 * 1024  # 1 PB
    assert check_disk_space(temp_dir, huge_space) == False

def test_validate_image(sample_image):
    """Test image validation."""
    assert validate_image(sample_image) == True
    
    # Test with corrupted image
    corrupted_image = Mock(spec=Image.Image)
    corrupted_image.verify.side_effect = Exception("Corrupted image")
    assert validate_image(corrupted_image) == False

def test_create_backup(temp_dir):
    """Test backup creation functionality."""
    # Create a test file
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, 'w') as f:
        f.write("test content")
    
    # Test successful backup
    backup_path = create_backup(test_file)
    assert backup_path is not None
    assert os.path.exists(backup_path)
    assert backup_path.endswith('.backup')
    
    # Test backup of non-existent file
    assert create_backup("nonexistent.txt") is None

def test_save_image_from_url_success(temp_dir):
    """Test successful image saving."""
    # Create a real bytes buffer
    img_buffer = BytesIO()
    sample_image = Image.new('RGB', (100, 100), color='red')
    sample_image.save(img_buffer, format='PNG')
    img_bytes = img_buffer.getvalue()
    
    # Mock response with actual image bytes
    mock_response = Mock()
    mock_response.content = img_bytes
    mock_response.status_code = 200
    
    with patch('requests.get', return_value=mock_response):
        filepath = save_image_from_url("http://example.com/image.png", temp_dir)
        assert os.path.exists(filepath)
        assert filepath.endswith('.png')

def test_save_image_from_url_download_error(temp_dir):
    """Test handling of download errors."""
    with patch('requests.get', side_effect=requests.RequestException("Download failed")):
        with pytest.raises(ImageSaveError) as exc_info:
            save_image_from_url("http://example.com/image.png", temp_dir)
        assert "Failed to download" in str(exc_info.value)

def test_save_image_from_url_invalid_image(temp_dir):
    """Test handling of invalid image data."""
    mock_response = Mock()
    mock_response.content = b"not an image"
    mock_response.status_code = 200
    
    with patch('requests.get', return_value=mock_response):
        with pytest.raises(ImageSaveError) as exc_info:
            save_image_from_url("http://example.com/image.png", temp_dir)
        assert "not a valid image" in str(exc_info.value)

def test_save_image_from_url_disk_space(temp_dir):
    """Test handling of insufficient disk space."""
    with patch('image_generation.utils.check_disk_space', return_value=False):
        with pytest.raises(ImageSaveError) as exc_info:
            save_image_from_url("http://example.com/image.png", temp_dir)
        assert "Insufficient disk space" in str(exc_info.value)

def test_validate_prompt():
    """Test prompt validation."""
    # Test valid prompt
    assert validate_prompt("Test prompt") == "Test prompt"
    
    # Test whitespace handling
    assert validate_prompt("  Test prompt  ") == "Test prompt"
    
    # Test empty prompt
    with pytest.raises(ValueError):
        validate_prompt("")
    
    with pytest.raises(ValueError):
        validate_prompt("   ")
    
    # Test non-string input
    with pytest.raises(ValueError):
        validate_prompt(None)
    
    with pytest.raises(ValueError):
        validate_prompt(123)
    
    # Test long prompt
    long_prompt = "a" * 501
    with pytest.raises(ValueError) as exc_info:
        validate_prompt(long_prompt)
    assert "too long" in str(exc_info.value)