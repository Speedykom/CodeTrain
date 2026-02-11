# Using LLM with CodeTrain

CodeTrain includes built-in support for calling LLMs via **OpenRouter**. This allows you to use various models (Claude, GPT-4, etc.) in your workflows.

## Setup

### 1. Get an API Key

1. Go to [OpenRouter](https://openrouter.ai/keys)
2. Create an account (or sign in)
3. Generate an API key
4. Copy the key

### 2. Configure Environment

```bash
# Copy the example config
cp .env.example .env

# Edit .env and add your API key
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

### 3. Use in Your Code

```python
from codetrain import call_llm_simple, call_llm

# Simple interface - just a prompt
response = call_llm_simple("What is Python?")
print(response)

# Full interface - with conversation history
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is CodeTrain?"},
]
response = call_llm(messages, temperature=0.7)
print(response)
```

## Configuration Options

All settings are in `.env`:

```bash
# Required
OPENROUTER_API_KEY=your-key-here

# Optional (with defaults)
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Optional - for OpenRouter rankings
OPENROUTER_HTTP_REFERRER=https://github.com/Speedykom/CodeTrain
OPENROUTER_SITE_NAME=CodeTrain
```

## Available Models

Popular models on OpenRouter:
- `anthropic/claude-3.5-sonnet` - Recommended
- `anthropic/claude-3-opus` - Most capable
- `openai/gpt-4o` - Latest GPT-4
- `openai/gpt-4o-mini` - Cheaper option
- `google/gemini-pro` - Google's model
- `meta-llama/llama-3.1-70b-instruct` - Open source

See all models at: https://openrouter.ai/models

## Examples with LLM

### 1. Hello World (`examples/hello_world.py`)

```python
USE_LLM = True  # Change this!

from codetrain import call_llm_simple

response = call_llm_simple(question)
```

### 2. Chatbot (`examples/chatbot.py`)

```python
USE_LLM = True

from codetrain import call_llm

response = call_llm(messages, temperature=0.8)
```

### 3. Translation (`examples/batch_translation.py`)

```python
USE_LLM = True

prompt = f"Translate to {language}: {text}"
translated = call_llm_simple(prompt, temperature=0.3)
```

## Error Handling

The `call_llm` functions will raise:

- `ValueError`: If API key is not configured
- `requests.RequestException`: If API call fails
- `KeyError`: If response format is unexpected

Always wrap in try/except for production code:

```python
try:
    response = call_llm_simple(prompt)
except ValueError as e:
    print(f"Config error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

## Cost Considerations

- OpenRouter provides a unified API for multiple providers
- Costs vary by model (check OpenRouter pricing)
- Set `max_tokens` to control costs:
  ```python
  call_llm_simple(prompt, max_tokens=150)
  ```

## Testing the Connection

```bash
# Test your setup
uv run python -c "
from codetrain import call_llm_simple
try:
    response = call_llm_simple('Say hello!')
    print('✓ Success:', response)
except Exception as e:
    print('✗ Error:', e)
"
```

## Legacy Support

The config system is designed to be "old school" - just a `.env` file with environment variables. No complex configuration classes or YAML files. Simple and straightforward!
