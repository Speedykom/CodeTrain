"""CodeTrain - A Minimalist Workflow Framework for the African Hustle.

Inspired by PocketFlow (https://github.com/The-Pocket/PocketFlow):
"A 100-line minimalist LLM framework for Agents, Task Decomposition, RAG, and more."

CodeTrain brings that same minimalist philosophy to African startups and developers,
translating complex workflow patterns into logistics-inspired concepts every
entrepreneur understands.

What is CodeTrain?
------------------
CodeTrain is a **minimalist workflow framework** that strips away complexity to reveal
the essential patterns of building AI and business automation pipelines. Following the
PocketFlow principle of "minimal code, maximum expressiveness," CodeTrain lets you
compose sophisticated workflows using just three concepts:

- **Job**: A unit of work (receive_order → prepare_order → ship_order)
- **Hustle**: Orchestrates multiple Jobs into a workflow
- **Manifest**: Carries data and state between Jobs

The Philosophy
--------------
Just as PocketFlow proves that powerful AI agent workflows need only 100 lines,
CodeTrain demonstrates that business process automation can be elegant, intuitive,
and culturally resonant.

Terminology:
- Job: Individual work unit (inspired by logistics delivery stops)
- Hustle: Orchestrates multiple jobs (the African entrepreneur's daily grind)
- receive_order: Load/prepare data from manifest
- prepare_order: Execute main work
- ship_order: Post-process, update manifest, and finalize
- manifest: Shared data store that travels through the workflow

Key Insight from PocketFlow:
"The best framework is the one that gets out of your way and lets you focus on
solving problems, not wrestling with complex abstractions."

CodeTrain embodies this by using logistics terminology that African entrepreneurs
already intuitively understand - every business is a hustle, every task is a job,
and every delivery needs a manifest.

Usage:
    import codetrain as ct

    class MyJob(ct.Job):
        def prepare_order(self, data):
            return process(data)

    job = MyJob()
    hustle = ct.Hustle(start=job)
    hustle.run(manifest)

Learn more: https://github.com/Speedykom/CodeTrain
Inspired by: https://github.com/The-Pocket/PocketFlow
"""

import asyncio
import warnings
import copy
import time


class Depot:
    """Base class for all jobs in a hustle."""

    def __init__(self):
        self.params = {}
        self.next_jobs = {}

    def set_params(self, params):
        """Set parameters for this job."""
        self.params = params

    def to(self, destination, action="default"):
        """Connect this job to the next one.

        Args:
            destination: The next Depot/Job to execute
            action: Action identifier for conditional routing
        """
        if action in self.next_jobs:
            warnings.warn(f"Overwriting action '{action}'")
        self.next_jobs[action] = destination
        return destination

    def receive_order(self, manifest):
        """Load data from manifest before executing."""
        pass

    def prepare_order(self, order_data):
        """Execute the main work on the order."""
        pass

    def ship_order(self, manifest, order_data, result):
        """Finalize and update manifest after work is done."""
        pass

    def _prepare_order(self, order_data):
        """Internal order preparation with execution."""
        return self.prepare_order(order_data)

    def _run(self, manifest):
        """Internal execution pipeline: receive -> prepare -> ship."""
        order_data = self.receive_order(manifest)
        result = self._prepare_order(order_data)
        return self.ship_order(manifest, order_data, result)

    def run(self, manifest):
        """Execute this job standalone (not part of a hustle)."""
        if self.next_jobs:
            warnings.warn("Use Hustle for connected jobs, not run() directly")
        return self._run(manifest)

    def __rshift__(self, other):
        """Allow: job_a >> job_b"""
        return self.to(other)

    def __sub__(self, action):
        """Allow conditional routing: job_a - "express" >> job_b"""
        if isinstance(action, str):
            return _JobConnection(self, action)
        raise TypeError("Action must be a string")


class _JobConnection:
    """Helper for conditional job routing."""

    def __init__(self, src, action):
        self.src = src
        self.action = action

    def __rshift__(self, tgt):
        return self.src.to(tgt, self.action)


class Job(Depot):
    """A single job unit with retry capability."""

    def __init__(self, max_retries=1, wait=0):
        super().__init__()
        self.max_retries = max_retries
        self.wait = wait
        self.cur_retry = 0

    def prepare_order_fallback(self, order_data, exc):
        """Handle failure after all retries exhausted."""
        raise exc

    def _prepare_order(self, order_data):
        """Prepare order with retry logic."""
        for self.cur_retry in range(self.max_retries):
            try:
                return self.prepare_order(order_data)
            except Exception as e:
                if self.cur_retry == self.max_retries - 1:
                    return self.prepare_order_fallback(order_data, e)
                if self.wait > 0:
                    time.sleep(self.wait)


class BatchJob(Job):
    """A job that processes multiple orders at once."""

    def _prepare_order(self, orders):
        """Prepare multiple orders sequentially."""
        if orders is None:
            return []
        return [super(BatchJob, self)._prepare_order(o) for o in orders]


class Hustle(Depot):
    """Orchestrates a hustle (workflow) through multiple jobs."""

    def __init__(self, start=None):
        super().__init__()
        self.start_job = start

    def start(self, start_job):
        """Set the starting job of the hustle."""
        self.start_job = start_job
        return start_job

    def get_next_job(self, current, action):
        """Determine the next job based on action."""
        nxt = current.next_jobs.get(action or "default")
        if not nxt and current.next_jobs:
            warnings.warn(f"Hustle ends: '{action}' not in {list(current.next_jobs)}")
        return nxt

    def _grind(self, manifest, params=None):
        """Execute the hustle from start to finish."""
        current = copy.copy(self.start_job)
        p = params or {**self.params}
        last_action = None

        while current:
            current.set_params(p)
            last_action = current._run(manifest)
            current = copy.copy(self.get_next_job(current, last_action))

        return last_action

    def _run(self, manifest):
        """Execute the hustle."""
        prep_res = self.receive_order(manifest)
        outcome = self._grind(manifest)
        return self.ship_order(manifest, prep_res, outcome)

    def ship_order(self, manifest, prep_res, exec_res):
        """Default ship_order just returns the result."""
        return exec_res


class BatchHustle(Hustle):
    """A hustle that runs multiple jobs in sequence."""

    def _run(self, manifest):
        """Execute multiple hustles."""
        pr = self.receive_order(manifest) or []
        for bp in pr:
            self._grind(manifest, {**self.params, **bp})
        return self.ship_order(manifest, pr, None)


class AsyncJob(Job):
    """Async-capable job for priority processing."""

    async def receive_order_async(self, manifest):
        """Async data loading."""
        pass

    async def prepare_order_async(self, order_data):
        """Async order preparation."""
        pass

    async def prepare_order_fallback_async(self, order_data, exc):
        """Async fallback on failure."""
        raise exc

    async def ship_order_async(self, manifest, order_data, result):
        """Async finalization."""
        pass

    async def _prepare_order(self, order_data):
        """Async preparation with retries."""
        for self.cur_retry in range(self.max_retries):
            try:
                return await self.prepare_order_async(order_data)
            except Exception as e:
                if self.cur_retry == self.max_retries - 1:
                    return await self.prepare_order_fallback_async(order_data, e)
                if self.wait > 0:
                    await asyncio.sleep(self.wait)

    async def run_async(self, manifest):
        """Execute async job standalone."""
        if self.next_jobs:
            warnings.warn("Use AsyncHustle for connected jobs")
        return await self._run_async(manifest)

    async def _run_async(self, manifest):
        """Async execution pipeline."""
        order_data = await self.receive_order_async(manifest)
        result = await self._prepare_order(order_data)
        return await self.ship_order_async(manifest, order_data, result)

    def _run(self, manifest):
        """Prevent sync execution of async jobs."""
        raise RuntimeError("Use run_async() for AsyncJob")


class AsyncBatchJob(AsyncJob, BatchJob):
    """Async batch job."""

    async def _prepare_order(self, orders):
        """Prepare multiple orders sequentially."""
        if orders is None:
            return []
        return [await super(AsyncBatchJob, self)._prepare_order(o) for o in orders]


class AsyncParallelBatchJob(AsyncJob, BatchJob):
    """Async batch job with parallel processing."""

    async def _prepare_order(self, orders):
        """Prepare multiple orders in parallel."""
        if orders is None:
            return []
        return await asyncio.gather(
            *(super(AsyncParallelBatchJob, self)._prepare_order(o) for o in orders)
        )


class AsyncHustle(Hustle, AsyncJob):
    """Async hustle for priority workflows."""

    async def _grind_async(self, manifest, params=None):
        """Async execution through jobs."""
        current = copy.copy(self.start_job)
        p = params or {**self.params}
        last_action = None

        while current:
            current.set_params(p)
            if isinstance(current, AsyncJob):
                last_action = await current._run_async(manifest)
            else:
                last_action = current._run(manifest)
            current = copy.copy(self.get_next_job(current, last_action))

        return last_action

    async def _run_async(self, manifest):
        """Async hustle execution."""
        prep_res = await self.receive_order_async(manifest)
        outcome = await self._grind_async(manifest)
        return await self.ship_order_async(manifest, prep_res, outcome)

    async def ship_order_async(self, manifest, prep_res, exec_res):
        """Default async ship_order."""
        return exec_res


class AsyncBatchHustle(AsyncHustle, BatchHustle):
    """Async batch hustle for multiple workflows."""

    async def _run_async(self, manifest):
        """Execute multiple async hustles."""
        pr = await self.receive_order_async(manifest) or []
        for bp in pr:
            await self._grind_async(manifest, {**self.params, **bp})
        return await self.ship_order_async(manifest, pr, None)


class AsyncParallelBatchHustle(AsyncHustle, BatchHustle):
    """Async batch hustle with parallel execution."""

    async def _run_async(self, manifest):
        """Execute multiple async hustles in parallel."""
        pr = await self.receive_order_async(manifest) or []
        await asyncio.gather(
            *(self._grind_async(manifest, {**self.params, **bp}) for bp in pr)
        )
        return await self.ship_order_async(manifest, pr, None)


# Legacy aliases for backwards compatibility (if needed)
Stop = Job
MultiDrop = BatchJob
Route = Hustle
FleetRoute = BatchHustle
ExpressStop = AsyncJob
ExpressMultiDrop = AsyncBatchJob
ExpressParallelMultiDrop = AsyncParallelBatchJob
ExpressRoute = AsyncHustle
ExpressFleetRoute = AsyncBatchHustle
ExpressParallelFleetRoute = AsyncParallelBatchHustle

# Main exports
__all__ = [
    # Core classes
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
]
