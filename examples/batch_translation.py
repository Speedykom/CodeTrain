"""Example 4: Batch Processing - Translation Workflow

This example demonstrates batch processing where we:
1. Take input text and target languages
2. Process each translation as a separate batch item
3. Save results to files

Uses LLM for actual translations when USE_LLM = True

CodeTrain Philosophy:
---------------------
Following PocketFlow's minimalist approach (https://github.com/The-Pocket/PocketFlow),
we use BatchJob to process multiple items efficiently.

The power of BatchJob:
- Automatically iterates over items
- Handles the loop for you
- Returns aggregated results
- Perfect for API calls, translations, processing lists

Key Insight:
- BatchJob extends Job but processes lists
- Each item in the list becomes a separate call to prepare_order
- Results are automatically collected into a list
- Saves you from writing boilerplate loops

Translated from: pocketflow-batch

To use with a real LLM:
1. Copy .env.example to .env
2. Add your OpenRouter API key to .env
3. Change USE_LLM = True below
"""

import os
import time
import codetrain as ct

# Set to True to use real LLM (requires OpenRouter API key)
USE_LLM = False

# Import call_llm when needed
if USE_LLM:
    from codetrain import call_llm_simple


class TranslateTextJob(ct.BatchJob):
    """Job to translate text into multiple languages.

    This BatchJob demonstrates:
    - Processing multiple translations in one Job
    - Automatic batching and result aggregation
    - Error handling for individual items

    The BatchJob parent class automatically:
    1. Iterates over the list from receive_order
    2. Calls prepare_order for each item
    3. Collects results into a list
    4. Passes all results to ship_order
    """

    def __init__(self, max_retries=1):
        super().__init__(max_retries=max_retries)

    def receive_order(self, manifest):
        """Prepare translation tasks for each language."""
        text = manifest.get("text", "(No text provided)")
        languages = manifest.get(
            "languages",
            [
                "Chinese",
                "Spanish",
                "Japanese",
                "German",
                "Russian",
                "Portuguese",
                "French",
                "Korean",
            ],
        )

        # Create a task for each language
        return [(text, lang) for lang in languages]

    def prepare_order(self, task):
        """Translate text to one language."""
        text, language = task

        if USE_LLM:
            # Real LLM translation
            prompt = f"""Translate the following text to {language}. 
Preserve the formatting and tone. Return only the translation, no explanations.

Text to translate:
{text}

Translation:"""
            try:
                # Add small delay to avoid rate limits
                time.sleep(1)
                translated = call_llm_simple(prompt, temperature=0.3)
                print(f"  ✓ Translated to {language}")
                return {"language": language, "translation": translated}
            except Exception as e:
                print(f"  ✗ Error translating to {language}: {e}")
                return {"language": language, "translation": f"[Error: {e}]"}
        else:
            # Simulated translation
            translations = {
                "Chinese": f"[中文翻译] {text[:50]}...",
                "Spanish": f"[Traducción española] {text[:50]}...",
                "Japanese": f"[日本語翻訳] {text[:50]}...",
                "German": f"[Deutsche Übersetzung] {text[:50]}...",
                "Russian": f"[Русский перевод] {text[:50]}...",
                "Portuguese": f"[Tradução portuguesa] {text[:50]}...",
                "French": f"[Traduction française] {text[:50]}...",
                "Korean": f"[한국어 번역] {text[:50]}...",
                "Swahili": f"[Tafsiri ya Kiswahili] {text[:50]}...",
                "Arabic": f"[الترجمة العربية] {text[:50]}...",
                "Yoruba": f"[Itumọ Yoruba] {text[:50]}...",
                "Zulu": f"[Ukuhumusha kwesiZulu] {text[:50]}...",
            }

            translated = translations.get(
                language, f"[Translation to {language}] {text[:50]}..."
            )

            print(f"  ✓ Translated to {language}")
            return {"language": language, "translation": translated}

    def ship_order(self, manifest, tasks, results):
        """Save all translations to files."""
        # Create output directory
        output_dir = manifest.get("output_dir", "translations")
        os.makedirs(output_dir, exist_ok=True)

        # Write each translation to a file
        saved_files = []
        for result in results:
            language = result["language"]
            translation = result["translation"]

            # Create filename
            filename = os.path.join(output_dir, f"translation_{language.upper()}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(translation)

            saved_files.append(filename)
            print(f"  ✓ Saved: {filename}")

        manifest["saved_files"] = saved_files
        # Return a string action (required for routing)
        return "done"


if __name__ == "__main__":
    # Sample text to translate
    sample_text = """
Welcome to CodeTrain!

CodeTrain is a Python library for building business workflows using 
logistics-inspired terminology. It helps startups and developers in 
Sub-Saharan Africa create powerful automation pipelines.

Key Features:
- Job: Individual work units (receive_order → prepare_order → ship_order)
- Hustle: Orchestrates multiple jobs
- Simple and intuitive API inspired by logistics

Get started today and build your hustle!
""".strip()

    # Configuration
    manifest = {
        "text": sample_text,
        "languages": ["Spanish", "French", "German", "Chinese", "Swahili"],
        "output_dir": "translations",
    }

    print("=" * 60)
    print("BATCH TRANSLATION WORKFLOW")
    print("=" * 60)
    print()
    print("This example demonstrates BatchJob:")
    print("  - One BatchJob processes multiple items")
    print("  - Automatic iteration and result collection")
    print("  - Perfect for translations, API calls, batch processing")
    print()
    print("CodeTrain Philosophy (inspired by PocketFlow):")
    print("  BatchJob handles the loop for you")
    print("  Each item → prepare_order → result")
    print("  All results collected automatically")
    print("=" * 60)
    print()

    if USE_LLM:
        print("🤖 Using real LLM via OpenRouter")
        print("   (This will make actual API calls with rate limiting)\n")
    else:
        print("📚 Using simulated translations")
        print("   (Set USE_LLM = True for real translations)\n")

    print(f"Original text ({len(sample_text)} characters):")
    print("-" * 60)
    print(sample_text[:200] + "..." if len(sample_text) > 200 else sample_text)
    print("-" * 60)

    print(f"\nTranslating to {len(manifest['languages'])} languages...")
    print(f"Languages: {', '.join(manifest['languages'])}\n")

    # Time the execution
    start_time = time.perf_counter()

    # Create and run the hustle
    translate_job = TranslateTextJob(max_retries=2)
    hustle = ct.Hustle(start=translate_job)
    hustle.run(manifest)

    end_time = time.perf_counter()
    duration = end_time - start_time

    print("\n" + "=" * 60)
    print(f"✓ Translation complete in {duration:.2f} seconds")
    print(f"✓ Saved {len(manifest['saved_files'])} files to: {manifest['output_dir']}")
    print("=" * 60)

    # Display the saved files
    print("\nGenerated files:")
    for filepath in manifest["saved_files"]:
        # Show first line of each translation
        try:
            with open(filepath, "r") as f:
                first_line = f.readline().strip()
                print(f"  - {filepath}")
                print(f"    Preview: {first_line[:60]}...")
        except:
            print(f"  - {filepath}")

    print("\n" + "=" * 60)
    print("Key Takeaway:")
    print("BatchJob automatically handles iteration for you.")
    print("Just return a list from receive_order, and prepare_order")
    print("will be called once for each item. Results are aggregated")
    print("into a list and passed to ship_order.")
    print()
    print("Learn more: https://github.com/Speedykom/CodeTrain")
    print("Inspired by: https://github.com/The-Pocket/PocketFlow")
    print("=" * 60)
    print()
    print("To use real translations:")
    print("1. Copy .env.example to .env")
    print("2. Get API key from https://openrouter.ai/keys")
    print("3. Add OPENROUTER_API_KEY to .env")
    print("4. Set USE_LLM = True in this file")
