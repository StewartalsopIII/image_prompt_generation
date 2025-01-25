"""
Utility functions for the image generation system.
"""

import os
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

def save_image_from_url(url: str, output_dir: str) -> str:
    """
    Download and save an image from a given URL.
    
    Args:
        url (str): URL of the image to download
        output_dir (str): Directory to save the image
        
    Returns:
        str: Path to the saved image file
        
    Raises:
        requests.RequestException: If image download fails
        IOError: If image saving fails
    """
    # Generate unique filename using timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'generated_image_{timestamp}.png'
    filepath = os.path.join(output_dir, filename)
    
    # Download and save the image
    response = requests.get(url)
    response.raise_for_status()
    
    image = Image.open(BytesIO(response.content))
    image.save(filepath)
    
    return filepath

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
        
    # Clean up whitespace
    cleaned_prompt = prompt.strip()
    
    if not cleaned_prompt:
        raise ValueError("Prompt cannot be empty or just whitespace")
        
    return cleaned_prompt