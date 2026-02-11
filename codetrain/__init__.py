"""CodeTrain - A Minimalist Workflow Framework for the African Hustle.

Inspired by PocketFlow: A 100-line minimalist LLM framework for Agents,
Task Decomposition, RAG, and more. (https://github.com/The-Pocket/PocketFlow)

What is CodeTrain?
------------------
CodeTrain is a minimalist workflow framework that strips away complexity to reveal
the essential patterns of building AI and business automation pipelines. Following
the PocketFlow philosophy of "minimal code, maximum expressiveness," CodeTrain
lets you compose sophisticated workflows using just three intuitive concepts:

- **Job**: A unit of work (receive_order → prepare_order → ship_order)
- **Hustle**: Orchestrates multiple Jobs into a workflow
- **Manifest**: Carries data and state between Jobs

The African Hustle Connection
-----------------------------
While PocketFlow uses abstract terminology, CodeTrain brings workflow concepts to
life through logistics-inspired naming that resonates with African entrepreneurs:

- **Job**: Like a delivery stop on a route
- **Hustle**: The daily grind of running a business
- **Manifest**: The paperwork that travels with every shipment

This makes CodeTrain not just a tool, but a mindset - every workflow is a hustle,
every task is a job, and success is about orchestrating them efficiently.

Core Philosophy
---------------
> "The best framework is the one that gets out of your way and lets you focus on
> solving business problems, not wrestling with complex abstractions."

CodeTrain follows the PocketFlow principle of minimal, expressive APIs:
- Just 3 methods to implement per Job
- Simple >> operator to connect Jobs
- Conditional routing with - "action" >>
- Batch processing built-in

Quick Example
-------------
    import codetrain as ct

    class ProcessPayment(ct.Job):
        def receive_order(self, manifest):
            return manifest['amount']

        def prepare_order(self, amount):
            return f"Processed ${amount}"

        def ship_order(self, manifest, amount, result):
            manifest['receipt'] = result
            return 'done'

    job = ProcessPayment()
    hustle = ct.Hustle(start=job)
    hustle.run({'amount': 100})

Installation
------------
    pip install git+https://github.com/Speedykom/CodeTrain.git

Learn More
----------
- Documentation: https://github.com/Speedykom/CodeTrain
- Inspired by: https://github.com/The-Pocket/PocketFlow
- PocketFlow GitHub: https://github.com/The-Pocket/PocketFlow

Designed for startups and developers in Sub-Saharan Africa.
"""

__version__ = "0.1.0"
__author__ = "Ricky Macharm"
__email__ = "Ricky.Macharm@speedykom.de"

# Logistics workflow engine with African startup flavor
# Job = individual unit of work
# Hustle = orchestrates multiple jobs
from .logistics import (
    Depot,
    Job,
    BatchJob,
    Hustle,
    BatchHustle,
    AsyncJob,
    AsyncBatchJob,
    AsyncParallelBatchJob,
    AsyncHustle,
    AsyncBatchHustle,
    AsyncParallelBatchHustle,
    # Legacy aliases
    Stop,
    MultiDrop,
    Route,
    FleetRoute,
    ExpressStop,
    ExpressMultiDrop,
    ExpressParallelMultiDrop,
    ExpressRoute,
    ExpressFleetRoute,
    ExpressParallelFleetRoute,
)

# LLM utilities
from .call_llm import call_llm, call_llm_simple
from . import config

__all__ = [
    # Core workflow classes
    "Depot",
    "Job",
    "BatchJob",
    "Hustle",
    "BatchHustle",
    "AsyncJob",
    "AsyncBatchJob",
    "AsyncParallelBatchJob",
    "AsyncHustle",
    "AsyncBatchHustle",
    "AsyncParallelBatchHustle",
    # Legacy aliases
    "Stop",
    "MultiDrop",
    "Route",
    "FleetRoute",
    "ExpressStop",
    "ExpressMultiDrop",
    "ExpressParallelMultiDrop",
    "ExpressRoute",
    "ExpressFleetRoute",
    "ExpressParallelFleetRoute",
    # LLM utilities
    "call_llm",
    "call_llm_simple",
    "config",
]
