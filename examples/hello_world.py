"""Example 1: Hello World - Simple Q&A Workflow with LLM

This is the simplest CodeTrain example - a single Job that asks a question
and gets an answer from an LLM.

CodeTrain Philosophy:
---------------------
Inspired by PocketFlow (https://github.com/The-Pocket/PocketFlow) - a 100-line minimalist
LLM framework. CodeTrain brings that same minimal, expressive power to African
startups through logistics-inspired terminology.

Key Insight:
- A Job has 3 phases: receive_order → prepare_order → ship_order
- Just like a delivery: receive → prepare → ship
- Minimal code, maximum expressiveness

Translated from: pocketflow-hello-world

To use with a real LLM:
1. Copy .env.example to .env
2. Add your OpenRouter API key to .env
3. Change USE_LLM = True below
"""

import codetrain as ct

# Set to True to use real LLM (requires OpenRouter API key)
USE_LLM = False

# Import call_llm when needed
if USE_LLM:
    from codetrain import call_llm_simple


class AnswerJob(ct.Job):
    """A simple job that answers a question using LLM or mock responses.

    Following the CodeTrain pattern:
    1. receive_order: Get the question from manifest
    2. prepare_order: Generate an answer (the actual work)
    3. ship_order: Store the answer back in manifest
    """

    def receive_order(self, manifest):
        """Load the question from the manifest."""
        return manifest["question"]

    def prepare_order(self, question):
        """Generate an answer using LLM or mock responses."""
        if USE_LLM:
            # Real LLM call via OpenRouter
            return call_llm_simple(question)
        else:
            # Simulated responses for demo
            answers = {
                "In one sentence, what's the end of universe?": "The end of the universe is still a mystery, but theories include heat death or a big crunch.",
                "What is Python?": "Python is a high-level programming language known for its simplicity and readability.",
                "What is CodeTrain?": "CodeTrain is PocketFlow for the African hustle - a minimalist workflow framework using logistics terminology.",
            }
            return answers.get(question, f"I don't know the answer to: {question}")

    def ship_order(self, manifest, question, answer):
        """Store the answer back in the manifest."""
        manifest["answer"] = answer
        return "done"


# Create the job and hustle
answer_job = AnswerJob()
qa_hustle = ct.Hustle(start=answer_job)

# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("HELLO WORLD - Q&A WITH CodeTrain")
    print("=" * 60)
    print()
    print("This example demonstrates the simplest CodeTrain workflow:")
    print("- One Job (AnswerJob)")
    print("- Three methods: receive_order, prepare_order, ship_order")
    print("- One Hustle to run it")
    print()

    if USE_LLM:
        print("🤖 Using real LLM via OpenRouter")
    else:
        print("📚 Using mock responses (set USE_LLM = True for real LLM)")
    print()

    # Example 1
    manifest = {
        "question": "In one sentence, what's the end of universe?",
        "answer": None,
    }

    qa_hustle.run(manifest)
    print(f"Q: {manifest['question']}")
    print(f"A: {manifest['answer']}")

    print("\n" + "-" * 60 + "\n")

    # Example 2
    manifest2 = {
        "question": "What is CodeTrain?",
        "answer": None,
    }

    qa_hustle.run(manifest2)
    print(f"Q: {manifest2['question']}")
    print(f"A: {manifest2['answer']}")

    print("\n" + "=" * 60)
    print("Key Takeaway:")
    print("A Job is just 3 methods that map to a delivery workflow:")
    print("  receive_order → prepare_order → ship_order")
    print("=" * 60)
    print()
    print("To use a real LLM:")
    print("1. Copy .env.example to .env")
    print("2. Get API key from https://openrouter.ai/keys")
    print("3. Add OPENROUTER_API_KEY to .env")
    print("4. Set USE_LLM = True in this file")
    print()
    print("Learn more: https://github.com/Speedykom/CodeTrain")
    print("Inspired by: https://github.com/The-Pocket/PocketFlow")
    print("=" * 60)
