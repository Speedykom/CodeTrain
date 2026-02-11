# Contributing to CodeTrain

Thank you for your interest in contributing to CodeTrain! 

## Our Philosophy

CodeTrain is inspired by [PocketFlow](https://github.com/The-Pocket/PocketFlow) - a 100-line minimalist 
LLM framework. We follow the same principle: **minimal code, maximum expressiveness**.

When contributing, remember:
- Keep it simple - if it needs 100 lines to explain, it's too complex
- Focus on the African hustle culture - logistics terminology should feel natural
- Every feature should make workflows more intuitive, not more complicated

## Development Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Setup

```bash
# Clone the repository
git clone https://github.com/Speedykom/CodeTrain.git
cd CodeTrain

# Install dependencies (creates .venv automatically)
uv sync --extra dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Run type checking
uv run mypy codetrain

# Format code
uv run ruff format .
```

## Project Structure

```
codetrain/
├── __init__.py          # Package exports and main documentation
├── logistics.py         # Core workflow engine (Job, Hustle, etc.)
├── call_llm.py          # OpenRouter LLM integration
└── config.py            # Environment configuration

examples/                # Example workflows
├── hello_world.py       # Simple Q&A
├── chatbot.py           # Interactive chat
├── ecommerce_fulfillment.py  # Order processing
├── web_crawler.py       # Multi-stage scraping
├── batch_translation.py # Batch processing
└── data_pipeline.py     # Data processing

tests/                   # Unit tests
docs/                    # Documentation
```

## Adding Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Add optional dependency
uv add --optional dev package-name
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=codetrain

# Run specific test file
uv run pytest tests/test_core.py

# Run specific test
uv run pytest tests/test_core.py::TestJob::test_job_execution
```

## Code Style

We follow PEP 8 with these specific rules:
- Line length: 88 characters (Black-compatible)
- Use double quotes for strings
- Use type hints where possible
- Document all public methods with docstrings

## Creating New Examples

When adding new examples:
1. Follow the logistics terminology (Job, Hustle, Manifest)
2. Include both mock and LLM versions (USE_LLM toggle)
3. Add African business context where relevant
4. Document the workflow with comments
5. Test with both `USE_LLM = False` and `USE_LLM = True`

Example template:
```python
"""Example: [Name]

[Description of what this example demonstrates]

Translated from: [pocketflow example if applicable]
"""

import codetrain as ct

# Set to True to use real LLM (requires OpenRouter API key)
USE_LLM = False

if USE_LLM:
    from codetrain import call_llm_simple


class MyJob(ct.Job):
    """Description of what this job does."""
    
    def receive_order(self, manifest):
        """Load data from manifest."""
        pass
    
    def prepare_order(self, data):
        """Execute main work."""
        if USE_LLM:
            return call_llm_simple(prompt)
        else:
            return mock_response
    
    def ship_order(self, manifest, data, result):
        """Finalize and update manifest."""
        manifest['result'] = result
        return 'done'


if __name__ == "__main__":
    # Example usage
    pass
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `uv run pytest`
5. Run linting: `uv run ruff check .`
6. Commit with clear messages
7. Push to your fork
8. Create a Pull Request

## Questions?

- Open an issue on GitHub
- Check existing examples for patterns
- Review PocketFlow documentation for workflow concepts

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn the framework
- Remember: we're building tools for African entrepreneurs

Thank you for contributing to CodeTrain!
