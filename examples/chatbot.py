"""Example 2: Interactive Chatbot with Memory

This example shows how to create a conversational chatbot that:
- Maintains conversation history
- Loops back to continue the conversation
- Exits when the user types 'exit'
- Uses LLM for intelligent responses

CodeTrain Philosophy:
---------------------
Following PocketFlow's minimalist approach (https://github.com/The-Pocket/PocketFlow),
we create a self-looping workflow using just one Job and one Hustle.

The magic is in the self-connection:
    chat_job - "continue" >> chat_job

This creates an infinite conversation loop that runs until the Job returns
None (when user types 'exit').

Key Insight:
- Jobs can connect to themselves for loops
- The manifest persists across iterations
- Perfect for interactive/conversational applications

Translated from: pocketflow-chat

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
    from codetrain import call_llm


class ChatJob(ct.Job):
    """Interactive chat job with conversation memory.

    This Job demonstrates several CodeTrain concepts:
    1. State persistence via manifest (conversation history)
    2. Conditional flow control (return None to exit)
    3. Self-looping workflows (chat_job - "continue" >> chat_job)
    """

    def receive_order(self, manifest):
        """Get user input and manage conversation history."""
        # Initialize messages if this is the first run
        if "messages" not in manifest:
            manifest["messages"] = []
            print("=" * 60)
            print("🤖 CodeTrain Chatbot")
            print("=" * 60)
            print()
            print("Welcome! This chatbot demonstrates CodeTrain's self-looping")
            print("workflows. Type 'exit' to end the conversation.")
            print()
            print("CodeTrain Philosophy:")
            print("  - One Job (ChatJob)")
            print("  - Self-connected: chat_job - 'continue' >> chat_job")
            print("  - Persistent state in manifest")
            print()
            print("Inspired by PocketFlow: https://github.com/The-Pocket/PocketFlow")
            print("=" * 60)

        # Get user input
        try:
            user_input = input("\nYou: ")
        except EOFError:
            # Handle piped input
            user_input = "exit"

        # Check if user wants to exit
        if user_input.lower() == "exit":
            return None

        # Add user message to history
        manifest["messages"].append({"role": "user", "content": user_input})

        # Return all messages for processing
        return manifest["messages"]

    def prepare_order(self, messages):
        """Generate a response using LLM or simple logic."""
        if messages is None:
            return None

        if USE_LLM:
            # Real LLM call with conversation history
            try:
                return call_llm(messages, temperature=0.8)
            except Exception as e:
                return f"[Error: {e}]"
        else:
            # Simple response logic (simulated)
            last_message = messages[-1]["content"].lower()

            # Simple keyword responses
            responses = {
                "hello": "Hello! How can I help you today? 👋",
                "hi": "Hi there! What can I do for you?",
                "how are you": "I'm doing great, thanks for asking! How about you?",
                "what is your name": "I'm CodeTrain Assistant, here to help you learn about workflows! 🚂",
                "help": "I can answer questions about CodeTrain, discuss coding, or just chat. What would you like to know?",
                "codetrain": "CodeTrain is PocketFlow for the African hustle - a minimalist workflow framework using logistics terminology!",
                "pocketflow": "PocketFlow is a 100-line minimalist LLM framework. CodeTrain brings that philosophy to African startups!",
                "job": "A Job is a unit of work with three steps: receive_order, prepare_order, and ship_order.",
                "hustle": "A Hustle orchestrates multiple Jobs into a workflow. It's the container for your business process!",
            }

            for keyword, response in responses.items():
                if keyword in last_message:
                    return response

            # Default responses
            defaults = [
                "That's interesting! Tell me more.",
                "I see. What else would you like to discuss?",
                "Fascinating! Can you elaborate on that?",
                "I'm learning so much from you! 🎓",
            ]
            import random

            return random.choice(defaults)

    def ship_order(self, manifest, messages, response):
        """Display response and update conversation history."""
        if messages is None or response is None:
            print("\n" + "=" * 60)
            print("👋 Goodbye! Thanks for chatting!")
            print("=" * 60)
            return None  # End the conversation

        # Print the assistant's response
        print(f"\nAssistant: {response}")

        # Add assistant message to history
        manifest["messages"].append({"role": "assistant", "content": response})

        # Loop back to continue the conversation
        return "continue"


# Create the chat job with self-loop
chat_job = ChatJob()
chat_job - "continue" >> chat_job  # Loop back to continue conversation

# Create the hustle
chat_hustle = ct.Hustle(start=chat_job)

# Start the chat
if __name__ == "__main__":
    manifest = {}

    if USE_LLM:
        print("\nUsing real LLM via OpenRouter\n")
    else:
        print("\nUsing simulated responses (set USE_LLM = True for real LLM)\n")

    chat_hustle.run(manifest)

    print("\n" + "=" * 60)
    print("Key Takeaway:")
    print("A Job can connect to itself to create loops:")
    print("  chat_job - 'continue' >> chat_job")
    print("This runs until the Job returns None to signal completion.")
    print("=" * 60)
