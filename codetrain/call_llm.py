"""LLM utility functions for CodeTrain examples.

Supports OpenRouter API for accessing various LLM models.
"""

import requests
from typing import List, Dict, Optional
from codetrain.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    OPENROUTER_HTTP_REFERRER,
    OPENROUTER_SITE_NAME,
)


def call_llm(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> str:
    """Call an LLM via OpenRouter API.

    Args:
        messages: List of message dicts with 'role' and 'content' keys
                 Example: [{"role": "user", "content": "Hello!"}]
        model: Model identifier (defaults to OPENROUTER_MODEL from config)
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens to generate

    Returns:
        The generated text response

    Raises:
        ValueError: If OPENROUTER_API_KEY is not configured
        requests.RequestException: If the API call fails
    """
    # Check for API key
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your-openrouter-api-key-here":
        raise ValueError(
            "OpenRouter API key not configured!\n"
            "Please set OPENROUTER_API_KEY in your .env file\n"
            "Get your key from: https://openrouter.ai/keys"
        )

    # Prepare headers
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    # Optional headers for OpenRouter rankings
    if OPENROUTER_HTTP_REFERRER:
        headers["HTTP-Referer"] = OPENROUTER_HTTP_REFERRER
    if OPENROUTER_SITE_NAME:
        headers["X-Title"] = OPENROUTER_SITE_NAME

    # Prepare request payload
    payload = {
        "model": model or OPENROUTER_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens:
        payload["max_tokens"] = max_tokens

    # Make API call
    response = requests.post(
        f"{OPENROUTER_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )

    # Check for errors
    response.raise_for_status()

    # Parse response
    data = response.json()

    if "choices" not in data or not data["choices"]:
        raise ValueError(f"Unexpected response format: {data}")

    return data["choices"][0]["message"]["content"]


def call_llm_simple(prompt: str, **kwargs) -> str:
    """Simple interface to call LLM with just a prompt string.

    Args:
        prompt: The text prompt to send
        **kwargs: Additional arguments passed to call_llm()

    Returns:
        The generated text response
    """
    messages = [{"role": "user", "content": prompt}]
    return call_llm(messages, **kwargs)


# Test function
if __name__ == "__main__":
    print("Testing OpenRouter LLM connection...")
    print(f"Using model: {OPENROUTER_MODEL}")
    print()

    try:
        response = call_llm_simple(
            "Say 'Hello from CodeTrain!' in a friendly way.",
            temperature=0.7,
        )
        print(f"✓ Success!")
        print(f"Response: {response}")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
    except requests.RequestException as e:
        print(f"✗ API error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
