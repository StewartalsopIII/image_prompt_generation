"""
Utility functions for the image generation system with enhanced error handling.
"""

import os
import shutil
from datetime import datetime
import requests
from PIL import Image
from PIL import UnidentifiedImageError
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageSaveError(Exception):
    """Custom exception for image saving related errors."""
    pass

def check_disk_space(filepath: str, required_bytes: int = 1024 * 1024 * 10) -> bool:
    """
    Check if there's enough disk space available.
    
    Args:
        filepath (str): Path where file will be saved
        required_bytes (int): Required space in bytes (default: 10MB)
        
    Returns:
        bool: True if enough space is available
    """
    try:
        total, used, free = shutil.disk_usage(os.path.dirname(filepath))
        return free > required_bytes
    except Exception as e:
        logger.warning(f"Failed to check disk space: {e}")
        return True  # Assume space is available if check fails

def validate_image(image: Image.Image) -> bool:
    """
    Validate that the image data is correct and not corrupted.
    
    Args:
        image (PIL.Image.Image): Image to validate
        
    Returns:
        bool: True if image is valid
    """
    try:
        # Try to perform a basic operation to verify image data
        image.verify()
        return True
    except Exception as e:
        logger.error(f"Image validation failed: {e}")
        return False

def create_backup(filepath: str) -> str:
    """
    Create a backup copy of an existing image.
    
    Args:
        filepath (str): Path to the file to backup
        
    Returns:
        str: Path to the backup file
    """
    if not os.path.exists(filepath):
        return None
        
    backup_path = f"{filepath}.backup"
    try:
        shutil.copy2(filepath, backup_path)
        return backup_path
    except Exception as e:
        logger.warning(f"Failed to create backup: {e}")
        return None

def save_image_from_url(url: str, output_dir: str) -> str:
    """
    Download and save an image from a given URL with enhanced error handling.
    
    Args:
        url (str): URL of the image to download
        output_dir (str): Directory to save the image
        
    Returns:
        str: Path to the saved image file
        
    Raises:
        ImageSaveError: If image download or saving fails
    """
    # Generate unique filename using timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'generated_image_{timestamp}.png'
    filepath = os.path.join(output_dir, filename)
    
    # Check available disk space
    if not check_disk_space(filepath):
        raise ImageSaveError("Insufficient disk space for saving the image")
    
    try:
        # Download the image
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Verify image data
        try:
            image = Image.open(BytesIO(response.content))
        except UnidentifiedImageError:
            raise ImageSaveError("Downloaded data is not a valid image")
        
        # Validate image
        if not validate_image(image):
            raise ImageSaveError("Image validation failed")
        
        # Create backup if file exists
        if os.path.exists(filepath):
            backup_path = create_backup(filepath)
            if backup_path:
                logger.info(f"Created backup at: {backup_path}")
        
        # Save the image
        image_copy = Image.open(BytesIO(response.content))  # Create new copy for saving
        image_copy.save(filepath)
        logger.info(f"Successfully saved image to: {filepath}")
        
        return filepath
        
    except requests.RequestException as e:
        raise ImageSaveError(f"Failed to download image: {str(e)}")
    except (IOError, OSError) as e:
        raise ImageSaveError(f"Failed to save image: {str(e)}")
    except Exception as e:
        raise ImageSaveError(f"Unexpected error while saving image: {str(e)}")

def validate_prompt(prompt: str) -> str:
    """
    Validate and clean up the user's text prompt.
    
    Args:
        prompt (str): User's input prompt
        
    Returns:
        str: Cleaned prompt
        
    Raises:
        ValueError: If prompt is empty or invalid
    """
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string")
        
    # Clean up whitespace and limit length
    cleaned_prompt = prompt.strip()
    
    if not cleaned_prompt:
        raise ValueError("Prompt cannot be empty or just whitespace")
    
    if len(cleaned_prompt) > 500:
        raise ValueError("Prompt is too long (maximum 500 characters)")
        
    return cleaned_prompt