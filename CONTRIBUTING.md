# Contributing to CodeTrain

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

### Adding Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Add optional dependency
uv add --optional dev package-name
```

### Running the Example

```bash
uv run python examples/basic_usage.py
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=codetrain

# Run specific test file
uv run pytest tests/test_core.py
```
