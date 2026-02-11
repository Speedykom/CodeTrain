# CodeTrain

A Python library for code training and learning.

## Installation

### Using uv (recommended)
```bash
uv pip install git+https://github.com/yourusername/CodeTrain.git
```

### Using pip
```bash
pip install git+https://github.com/yourusername/CodeTrain.git
```

## Development Setup (with uv)

```bash
# Clone the repository
git clone https://github.com/yourusername/CodeTrain.git
cd CodeTrain

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Run tests
uv run pytest

# Run example
uv run python examples/basic_usage.py
```

## Usage

```python
import codetrain

# Your code here
print(codetrain.hello())
```

## Features

- Feature 1
- Feature 2
- Feature 3
