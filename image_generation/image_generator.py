"""
Core module for generating images using the Replicate API with enhanced error handling and retries.
"""

import time
import replicate
from typing import Optional, Dict, Tuple
from requests.exceptions import RequestException
import logging

from image_generation.config import load_config
from image_generation.utils import validate_prompt, save_image_from_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom exception for API-related errors."""
    pass

class ImageGenerator:
    """
    Handles image generation using the Replicate API with robust error handling and retries.
    """
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        """
        Initialize the image generator with configuration.
        
        Args:
            max_retries (int): Maximum number of retry attempts for failed API calls
            base_delay (float): Base delay in seconds between retries (will be exponentially increased)
        """
        self.config = load_config()
        self.client = replicate.Client(api_token=self.config['api_token'])
        self.max_retries = max_retries
        self.base_delay = base_delay
        
    def _handle_api_error(self, error: Exception) -> Tuple[bool, str]:
        """
        Handle different types of API errors and determine if retry is appropriate.
        
        Args:
            error: The caught exception
            
        Returns:
            Tuple[bool, str]: (should_retry, error_message)
        """
        if isinstance(error, replicate.exceptions.ModelError):
            return False, f"Model error: {str(error)}"
        elif isinstance(error, replicate.exceptions.ReplicateError):
            if "rate limit" in str(error).lower():
                return True, "Rate limit exceeded"
            elif "unauthorized" in str(error).lower():
                return False, "Invalid API token"
            else:
                return True, f"API error: {str(error)}"
        elif isinstance(error, RequestException):
            return True, f"Network error: {str(error)}"
        else:
            return False, f"Unexpected error: {str(error)}"

    def generate_image(self, prompt: str) -> Dict[str, str]:
        """
        Generate an image from a text prompt with retry mechanism.
        
        Args:
            prompt (str): Text description of the image to generate
            
        Returns:
            dict: Dictionary containing:
                - 'filepath': Path to the saved image
                - 'prompt': Original prompt used
                
        Raises:
            ValueError: If prompt is invalid
            APIError: If all retry attempts fail
        """
        # Validate and clean the prompt
        cleaned_prompt = validate_prompt(prompt)
        
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    delay = self.base_delay * (2 ** (attempt - 1))  # Exponential backoff
                    logger.info(f"Retry attempt {attempt}/{self.max_retries} after {delay:.1f}s delay")
                    time.sleep(delay)
                
                # Generate image using Replicate's API
                output = self.client.run(
                    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                    input={"prompt": cleaned_prompt}
                )
                
                # Save the generated image
                image_url = output[0]  # First URL in the output
                filepath = save_image_from_url(image_url, self.config['output_dir'])
                
                logger.info(f"Successfully generated image after {attempt + 1} attempt(s)")
                return {
                    'filepath': filepath,
                    'prompt': cleaned_prompt
                }
                
            except Exception as e:
                should_retry, error_message = self._handle_api_error(e)
                last_error = APIError(error_message)
                
                if not should_retry or attempt == self.max_retries:
                    logger.error(f"Failed to generate image: {error_message}")
                    raise last_error
                
                logger.warning(f"Attempt {attempt + 1} failed: {error_message}")

def main():
    """CLI interface for testing image generation."""
    try:
        generator = ImageGenerator()
        prompt = input("Enter image prompt: ")
        result = generator.generate_image(prompt)
        print(f"Image generated successfully!\nSaved to: {result['filepath']}")
    except (ValueError, APIError) as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()