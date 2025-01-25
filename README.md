# Image Prompt Generation System

This project implements a photo-realistic image generation system using the Replicate API. It provides a simple yet powerful interface for generating images from text prompts, with plans to evolve into a full chatbot interface.

## Project Structure

The system is organized into several key components:
- `config.py`: Configuration management and environment variable handling
- `utils.py`: Utility functions for image handling and prompt validation
- `image_generator.py`: Core image generation functionality using Replicate API

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Add your Replicate API token

## Development Status

The project is currently in initial development, following a structured plan for feature implementation. See `plan.md` for detailed development roadmap.