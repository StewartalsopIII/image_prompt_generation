"""
Core module for generating images using the Replicate API.
"""

import replicate
from typing import Optional, Dict

from .config import load_config
from .utils import validate_prompt, save_image_from_url

class ImageGenerator:
    """
    Handles image generation using the Replicate API.
    """
    
    def __init__(self):
        """Initialize the image generator with configuration."""
        self.config = load_config()
        self.client = replicate.Client(api_token=self.config['api_token'])
        
    def generate_image(self, prompt: str) -> Dict[str, str]:
        """
        Generate an image from a text prompt.
        
        Args:
            prompt (str): Text description of the image to generate
            
        Returns:
            dict: Dictionary containing:
                - 'filepath': Path to the saved image
                - 'prompt': Original prompt used
                
        Raises:
            ValueError: If prompt is invalid
            replicate.exceptions.ReplicateError: If API call fails
        """
        # Validate and clean the prompt
        cleaned_prompt = validate_prompt(prompt)
        
        # Generate image using Replicate's API
        output = self.client.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={"prompt": cleaned_prompt}
        )
        
        # Save the generated image
        image_url = output[0]  # First URL in the output
        filepath = save_image_from_url(image_url, self.config['output_dir'])
        
        return {
            'filepath': filepath,
            'prompt': cleaned_prompt
        }

def main():
    """CLI interface for testing image generation."""
    try:
        generator = ImageGenerator()
        prompt = input("Enter image prompt: ")
        result = generator.generate_image(prompt)
        print(f"Image generated successfully!\nSaved to: {result['filepath']}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()