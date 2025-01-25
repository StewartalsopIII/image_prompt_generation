"""
Configuration module for the image generation system.
Handles loading and validation of environment variables.
"""

import os
from dotenv import load_dotenv

def load_config():
    """
    Load and validate environment variables required for the application.
    
    Returns:
        dict: Configuration dictionary containing validated settings
    
    Raises:
        ValueError: If required environment variables are missing
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get Replicate API token
    api_token = os.getenv('REPLICATE_API_TOKEN')
    if not api_token:
        raise ValueError('REPLICATE_API_TOKEN must be set in environment variables')
        
    # Get optional configuration values with defaults
    output_dir = os.getenv('OUTPUT_DIR', 'generated_images')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    return {
        'api_token': api_token,
        'output_dir': output_dir
    }
