# LLM Development Learnings

## 1. Insights and Patterns
* Document key observations about the project or codebase
* Examples:
   * "When setting up Python virtual environments, always verify the environment activation with 'which python' to ensure correct package installation paths."
   * "The replicate package requires explicit virtual environment activation to function properly."
   * "Package installation status should be verified with 'pip list' before running scripts."

## 2. AI Behavior Notes
* Record any issues or limitations observed in the AI's behavior
* Examples:
   * "When executing multiple shell commands, Claude performs better with single-command execution rather than combining commands with &&."
   * "File editing works best with precise, minimal changes rather than attempting to replace large sections."
   * "Claude needs to verify file content after each edit to ensure changes are applied correctly."

## 3. Design Decisions
* Record architectural and implementation choices
* Examples:
   * "Implemented separate modules (config.py, utils.py, image_generator.py) to maintain clear separation of concerns and improve maintainability."
   * "Used environment variables (.env) for sensitive configuration to enhance security and flexibility."
   * "Chose to implement comprehensive error handling in each module to ensure robust operation."

## 4. Mistakes and Avoidance
* Document errors or issues that occurred and how they were resolved
* Examples:
   * "Nested virtual environments caused package import issues. Always deactivate existing virtual environments before activating a new one."
   * "ModuleNotFoundError was resolved by ensuring proper virtual environment activation and verification."
   * "File editing attempts that replace too much content at once are prone to errors - make smaller, targeted changes."

## 5. Validation Lessons
* Note effective validation strategies and steps
* Examples:
   * "Using 'which python' and 'pip list' commands helps verify correct virtual environment setup and package installation."
   * "Check virtual environment status in terminal prompt (venv) before executing Python commands."
   * "Verify successful deactivation of virtual environments before creating or activating new ones."

## 6. General Notes for Continuity
* Project context and important background information
* Examples:
   * "The project uses the Replicate API with SDXL model for image generation. API tokens must be properly configured in .env file before use."
   * "Virtual environment management is crucial for this project - always ensure clean activation/deactivation cycles."

## Updates Log
[2025-01-25] - Initial setup and documentation
[2025-01-25] - Added virtual environment management learnings
[2025-01-25] - Added file editing and validation strategies