# What is CodeTrain?

## The Short Answer

**CodeTrain is PocketFlow for the African hustle culture.**

Just as [PocketFlow](https://github.com/The-Pocket/PocketFlow) strips complex AI agent workflows down to their essence in 100 lines, CodeTrain brings that same minimalist elegance to African startups and developers through logistics-inspired concepts.

## The Philosophy

### From PocketFlow

[PocketFlow](https://github.com/The-Pocket/PocketFlow) is a 100-line minimalist LLM framework for:
- Agents
- Task Decomposition  
- RAG (Retrieval-Augmented Generation)
- And more

Its core insight:

> "The best framework is the one that gets out of your way and lets you focus on solving problems, not wrestling with complex abstractions."

### To CodeTrain

CodeTrain applies this philosophy to business workflows, but with a twist: **African logistics terminology**.

Why? Because every entrepreneur in Sub-Saharan Africa understands:
- A **Job** is a task that needs doing
- A **Hustle** is the daily grind of running a business
- A **Manifest** is the paperwork that travels with every delivery

This isn't just naming - it's a **mindset shift**. When you build workflows with CodeTrain, you're not just writing code; you're orchestrating a hustle.

## The Pattern

Both frameworks follow the same elegant pattern:

### PocketFlow (Abstract)
```python
class Node:
    def prep(self, shared): ...
    def exec(self, prep_res): ...
    def post(self, shared, prep_res, exec_res): ...
```

### CodeTrain (Logistics)
```python
class Job:
    def receive_order(self, manifest): ...
    def prepare_order(self, order_data): ...
    def ship_order(self, manifest, order_data, result): ...
```

**Same pattern. Different vocabulary. Same power.**

## Why This Matters

### For African Developers

You don't need to learn abstract computer science terminology to build powerful workflows. You already know:
- How to receive an order
- How to prepare goods
- How to ship them out

CodeTrain maps workflow concepts to your existing mental models.

### For Startups

Your business processes ARE workflows:
- Customer onboarding → Jobs: Verify → Setup → Welcome
- Order fulfillment → Jobs: Receive → Pick → Pack → Ship
- Content creation → Jobs: Research → Draft → Edit → Publish

CodeTrain lets you model these naturally.

## The Core Abstractions

### 1. Job

A **Job** is the atomic unit of work. It has three phases:

1. **receive_order(manifest)** - Load what you need
2. **prepare_order(data)** - Do the work
3. **ship_order(manifest, data, result)** - Deliver results

Think of it like a delivery stop:
- You receive the order details
- You prepare the package
- You ship it out

### 2. Hustle

A **Hustle** orchestrates multiple Jobs. It's the container that runs your workflow from start to finish.

```python
verify_payment = VerifyPaymentJob()
prepare_package = PreparePackageJob()
ship_order = ShipOrderJob()

# Connect them
verify_payment >> prepare_package >> ship_order

# Create the hustle
fulfillment_hustle = Hustle(start=verify_payment)
```

### 3. Manifest

The **Manifest** is your shared data store. It travels through every Job in the Hustle, collecting data and state.

```python
manifest = {
    'order_id': '12345',
    'customer': 'Ama Mensah',
    'items': ['laptop', 'mouse'],
    'payment_status': 'confirmed',
    # ... gets updated by each Job
}
```

## What Makes It Powerful

### Composability

Jobs are LEGO blocks. Connect them however you need:

```python
# Sequential
job_a >> job_b >> job_c

# Conditional routing
router - "success" >> job_success
router - "failure" >> job_failure

# Self-looping (for conversations)
chat_job - "continue" >> chat_job
```

### Batching

Process multiple items at once:

```python
class TranslateJob(BatchJob):
    def prepare_order(self, text):
        return translate(text)

# Automatically processes all items
translate_job.run([text1, text2, text3])
```

### Async Support

For I/O-bound operations:

```python
class AsyncFetchJob(AsyncJob):
    async def prepare_order_async(self, url):
        return await fetch(url)
```

## Real-World Examples

### PocketFlow Examples → CodeTrain

| PocketFlow Example | CodeTrain Equivalent | Business Context |
|-------------------|---------------------|------------------|
| Hello World Q&A | `hello_world.py` | Customer service bot |
| Interactive Chat | `chatbot.py` | Sales assistant |
| Web Crawler | `web_crawler.py` | Market research |
| Batch Translation | `batch_translation.py` | Content localization |
| Data Pipeline | `data_pipeline.py` | Business analytics |

## The 100-Line Promise

PocketFlow proved you don't need thousands of lines for a workflow framework.

CodeTrain's core (`logistics.py`) is similarly lean:
- **Depot** - Base class
- **Job** - Unit of work with retries
- **BatchJob** - Multi-item processing
- **Hustle** - Workflow orchestration
- **Async variants** - For modern async code

Everything else is examples, documentation, and LLM integrations.

## Getting Started

```bash
# Install
pip install git+https://github.com/Speedykom/CodeTrain.git

# Run an example
python examples/hello_world.py
```

## The Vision

**Every African startup should be able to automate their hustle.**

CodeTrain makes this possible by:
1. **Lowering barriers** - Intuitive terminology
2. **Building on proven patterns** - PocketFlow foundation
3. **Staying minimal** - No unnecessary complexity
4. **Empowering creators** - You focus on business logic

## Learn More

- **PocketFlow Substack**: https://github.com/The-Pocket/PocketFlow
- **PocketFlow GitHub**: https://github.com/The-Pocket/PocketFlow
- **CodeTrain GitHub**: https://github.com/Speedykom/CodeTrain

## Summary

> **CodeTrain = PocketFlow philosophy + African logistics terminology**

It's the same powerful workflow patterns, expressed in the language of the hustle. Because when you're building the next great African startup, your tools should work as hard as you do.

---

*"The best framework is the one that gets out of your way."* - PocketFlow

*"The best hustle is the one that runs itself."* - CodeTrain
