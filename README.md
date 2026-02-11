# CodeTrain

CodeTrain is inspired by the philosophy of PocketFlow: **A 100-line minimalist LLM framework 
for Agents, Task Decomposition, RAG, and more.**

Just as PocketFlow strips away complexity to reveal the essential patterns of AI workflows,
CodeTrain brings that same elegance to African startups and developers through intuitive,
logistics-based abstractions.

## What is CodeTrain?

CodeTrain is a **minimalist workflow framework** that lets you build powerful AI and business
automation pipelines using concepts every entrepreneur understands: Jobs, Hustles, and Manifests.

Think of it as **PocketFlow for the African hustle culture** - where:
- A **Job** is a unit of work (like a delivery stop)
- A **Hustle** orchestrates multiple Jobs into a workflow
- A **Manifest** carries data between stages

## Core Philosophy

> "The best framework is the one that gets out of your way and lets you focus on solving 
> business problems, not wrestling with complex abstractions."

CodeTrain follows the PocketFlow principle: **minimal code, maximum expressiveness**.

## Installation

### Using uv (recommended)
```bash
uv pip install git+https://github.com/Speedykom/CodeTrain.git
```

### Using pip
```bash
pip install git+https://github.com/Speedykom/CodeTrain.git
```

## Using with opencode (AI Agent)

CodeTrain includes a comprehensive **SKILL.md** file for AI agents using [opencode](https://opencode.ai/).

### Global SKILL (Recommended)

To use CodeTrain across all your projects:

```bash
# Download the SKILL.md to your opencode config
curl -o ~/.config/opencode/skills/codetrain/SKILL.md https://raw.githubusercontent.com/Speedykom/CodeTrain/main/SKILL.md
```

Or manually:
1. Create directory: `mkdir -p ~/.config/opencode/skills/codetrain/`
2. Copy `SKILL.md` from this repo to that directory
3. The AI agent will now understand CodeTrain in all your projects

### Project-Specific SKILL

For a single project, copy `SKILL.md` to your project root:

```bash
# In your project directory
cp /path/to/codetrain/SKILL.md ./SKILL.md
```

### What the SKILL.md Covers

The CodeTrain SKILL.md teaches AI agents:
- **Agentic Coding Workflow**: 8-step development process
- **CodeTrain Philosophy**: Job → Hustle → Manifest pattern
- **OpenRouter Integration**: How to use config.py for API keys
- **Design Patterns**: Workflow, Agent, Map Reduce, RAG
- **Project Structure**: How to organize CodeTrain projects
- **Best Practices**: Common patterns and mistakes to avoid

**Example AI prompt:**
```
I want to build a workflow that processes customer orders using CodeTrain.
The workflow should: receive order, validate payment, prepare package, and ship.
Please create the Jobs and Hustle for this.
```

The AI agent will use the SKILL.md to generate proper CodeTrain code with:
- ✅ Proper Job structure (receive_order, prepare_order, ship_order)
- ✅ OpenRouter integration via config.py
- ✅ Appropriate design patterns
- ✅ Best practices for reliability

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Speedykom/CodeTrain.git
cd CodeTrain

# Create virtual environment and install dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Run an example
uv run python examples/hello_world.py
```

## Core Concepts

CodeTrain uses logistics-inspired terminology that resonates with African entrepreneurs:

| Concept | Description |
|---------|-------------|
| **Job** | Individual unit of work (receive → prepare → ship) |
| **Hustle** | Orchestrates multiple jobs into a workflow |
| **Manifest** | Shared data store passed between jobs |
| **>>** | Connect jobs in sequence |
| **- "action" >>** | Conditional routing between jobs |

## Quick Start

```python
import codetrain as ct

# Define a Job
class GreetingJob(ct.Job):
    def receive_order(self, manifest):
        return manifest.get("name", "World")
    
    def prepare_order(self, name):
        return f"Hello, {name}!"
    
    def ship_order(self, manifest, name, greeting):
        manifest["greeting"] = greeting
        return "done"

# Run the job
job = GreetingJob()
manifest = {"name": "Africa"}
job.run(manifest)

print(manifest["greeting"])  # Hello, Africa!
```

## Examples

### 1. Hello World (`examples/hello_world.py`)
Simple Q&A workflow - the basics of CodeTrain.

```bash
uv run python examples/hello_world.py
```

### 2. Interactive Chatbot (`examples/chatbot.py`)
Conversational AI with memory and self-looping.

```bash
uv run python examples/chatbot.py
```

### 3. E-Commerce Fulfillment (`examples/ecommerce_fulfillment.py`)
Order processing workflow with conditional routing (standard vs express delivery).

```bash
uv run python examples/ecommerce_fulfillment.py
```

### 4. Web Crawler (`examples/web_crawler.py`)
Multi-stage web scraping: crawl → analyze → report.

```bash
uv run python examples/web_crawler.py
```

### 5. Batch Translation (`examples/batch_translation.py`)
Process items in batches - translates text to multiple languages simultaneously.

```bash
uv run python examples/batch_translation.py
```

### 6. Data Pipeline (`examples/data_pipeline.py`)
Data processing workflow: load → clean → transform → report.

```bash
uv run python examples/data_pipeline.py
```

## Features

- **Simple API**: Just 3 methods per job (receive_order, prepare_order, ship_order)
- **Composable**: Chain jobs with `>>` operator
- **Conditional Routing**: Branch workflows with `- "action" >>`
- **Batch Processing**: Handle multiple items with BatchJob
- **Error Handling**: Built-in retry mechanism
- **Async Support**: AsyncJob and AsyncHustle for concurrent operations

## Architecture

```
Job (Base)
├── receive_order(manifest) → Load data
├── prepare_order(data) → Execute work
└── ship_order(manifest, data, result) → Finalize

BatchJob (Job)
└── Processes multiple items in batches

Hustle
└── Orchestrates connected jobs

AsyncJob / AsyncHustle
└── Async/await support for concurrent operations
```

## PocketFlow Connection

CodeTrain draws inspiration from [PocketFlow](https://github.com/The-Pocket/PocketFlow), 
the minimalist LLM framework. While PocketFlow provides the conceptual foundation for 
AI agent workflows, CodeTrain adapts these patterns for the African context with:

- **Logistics terminology** (Jobs, Hustles, Manifests)
- **African startup culture** embedded in naming
- **Local examples** relevant to Sub-Saharan entrepreneurs

## Resources

### Documentation
- **SKILL.md** - Comprehensive guide for AI agents (see file in repo root)
- **docs/PHILOSOPHY.md** - Deep dive into CodeTrain's design philosophy
- **docs/LLM_SETUP.md** - How to configure OpenRouter integration
- **examples/** - 6 complete working examples

### Links
- **CodeTrain GitHub**: https://github.com/Speedykom/CodeTrain
- **PocketFlow GitHub**: https://github.com/The-Pocket/PocketFlow

### For AI Agents
The **SKILL.md** file in this repository contains everything an AI agent needs to know to build CodeTrain workflows effectively. It includes:
- Complete development workflow
- CodeTrain-specific patterns
- OpenRouter integration details
- Design patterns and best practices

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](LICENSE) file.

---

**Inspired by [PocketFlow](https://github.com/The-Pocket/PocketFlow)** - A 100-line minimalist 
LLM framework for Agentic Coding. Let Agents build Agents!
