"""Configuration management for CodeTrain.

Old-school config - loads from environment variables and .env file.
"""

import os
from pathlib import Path


def load_env_file(filepath=".env"):
    """Load environment variables from .env file."""
    env_path = Path(filepath)
    if not env_path.exists():
        return

    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


# Load .env file
load_env_file()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")

# Optional: HTTP Referrer for OpenRouter rankings
OPENROUTER_HTTP_REFERRER = os.getenv(
    "OPENROUTER_HTTP_REFERRER", "https://github.com/Speedykom/CodeTrain"
)

# Optional: Site name for OpenRouter
OPENROUTER_SITE_NAME = os.getenv("OPENROUTER_SITE_NAME", "CodeTrain")


# Validate configuration
def validate_config():
    """Check if required configuration is present."""
    missing = []
    if not OPENROUTER_API_KEY:
        missing.append("OPENROUTER_API_KEY")

    if missing:
        raise ValueError(
            f"Missing required configuration: {', '.join(missing)}\n"
            f"Please set these in your .env file or environment variables."
        )

    return True
