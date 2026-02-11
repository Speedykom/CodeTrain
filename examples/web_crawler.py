"""Example 3: Web Crawler Workflow

This example demonstrates a three-stage workflow:
1. Crawl a website and extract page content
2. Analyze the content in batches
3. Generate a summary report

CodeTrain Philosophy:
---------------------
Inspired by PocketFlow (https://github.com/The-Pocket/PocketFlow), this example shows
how to compose multiple Jobs into a workflow using the >> operator.

The pattern:
    crawl >> analyze >> report

Each Job passes data through the manifest, building up results stage by stage.
This is the essence of workflow orchestration - breaking complex tasks into
simple, composable units.

Key Insight:
- Complex workflows = simple Jobs + connections
- Each Job does one thing well
- The manifest carries state between Jobs
- BatchJob processes multiple items efficiently

Translated from: pocketflow-tool-crawler
"""

import codetrain as ct
from urllib.parse import urljoin, urlparse
import re


class CrawlWebsiteJob(ct.Job):
    """Job to crawl a website and extract content.

    This Job demonstrates:
    - Receiving configuration from manifest
    - Performing I/O operations (web crawling)
    - Storing results back in manifest
    """

    def receive_order(self, manifest):
        """Get crawl parameters from manifest."""
        return manifest.get("base_url"), manifest.get("max_pages", 10)

    def prepare_order(self, inputs):
        """Simulate web crawling."""
        base_url, max_pages = inputs

        if not base_url:
            return []

        # Simulate crawling - in real use, you'd use requests/BeautifulSoup
        # For demo, we'll create mock crawl results
        pages_crawled = min(max_pages, 5)  # Cap at 5 for demo

        results = []
        for i in range(pages_crawled):
            page_data = {
                "url": f"{base_url}/page{i + 1}",
                "title": f"Sample Page {i + 1}",
                "content": f"This is sample content for page {i + 1}. "
                f"It contains information about topic {i + 1}. "
                f"Keywords: python, coding, tutorial.",
                "html": f"<html><body><h1>Page {i + 1}</h1><p>Content here...</p></body></html>",
            }
            results.append(page_data)

        print(f"✓ Crawled {len(results)} pages from {base_url}")
        return results

    def ship_order(self, manifest, inputs, crawl_results):
        """Store crawl results in manifest."""
        manifest["crawl_results"] = crawl_results
        return "default"


class AnalyzeContentJob(ct.BatchJob):
    """Job to analyze crawled content in batches.

    This BatchJob demonstrates:
    - Processing multiple items at once
    - Splitting work into batches
    - Aggregating results
    """

    def receive_order(self, manifest):
        """Split crawl results into batches."""
        results = manifest.get("crawl_results", [])

        # Process in batches of 2 pages
        batch_size = 2
        batches = [
            results[i : i + batch_size] for i in range(0, len(results), batch_size)
        ]

        print(f"✓ Split {len(results)} pages into {len(batches)} batches")
        return batches

    def prepare_order(self, batch):
        """Analyze a batch of pages."""
        analyzed = []

        for page in batch:
            # Simple analysis (in real use, you'd use NLP/LLM)
            content = page.get("content", "")
            words = content.lower().split()

            # Extract keywords (words longer than 5 chars)
            keywords = [w for w in words if len(w) > 5]

            analysis = {
                "summary": f"Page about: {page.get('title', 'Unknown')}",
                "word_count": len(words),
                "keywords": list(set(keywords))[:5],  # Top 5 unique keywords
                "content_type": "article" if len(words) > 20 else "short",
            }

            analyzed.append(
                {"url": page["url"], "title": page["title"], "analysis": analysis}
            )

        return analyzed

    def ship_order(self, manifest, batches, results_list):
        """Combine all batch results."""
        # Flatten results from all batches
        all_results = []
        for batch_results in results_list:
            all_results.extend(batch_results)

        manifest["analyzed_results"] = all_results
        print(f"✓ Analyzed {len(all_results)} pages total")
        return "default"


class GenerateReportJob(ct.Job):
    """Job to generate a summary report.

    This final Job demonstrates:
    - Consuming data from previous Jobs
    - Formatting results
    - Presenting output
    """

    def receive_order(self, manifest):
        """Get analyzed results."""
        return manifest.get("analyzed_results", [])

    def prepare_order(self, results):
        """Generate a formatted report."""
        if not results:
            return "No results to report"

        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("WEB CRAWL ANALYSIS REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"\nTotal pages analyzed: {len(results)}\n")

        for page in results:
            report_lines.append(f"\nPage: {page['url']}")
            report_lines.append(f"Title: {page['title']}")

            analysis = page.get("analysis", {})
            report_lines.append(f"Summary: {analysis.get('summary', 'N/A')}")
            report_lines.append(f"Word Count: {analysis.get('word_count', 0)}")
            report_lines.append(f"Keywords: {', '.join(analysis.get('keywords', []))}")
            report_lines.append(
                f"Content Type: {analysis.get('content_type', 'unknown')}"
            )
            report_lines.append("-" * 60)

        return "\n".join(report_lines)

    def ship_order(self, manifest, results, report):
        """Store and display the report."""
        manifest["report"] = report
        print("\n" + report)
        return "default"


def create_crawler_hustle():
    """Create and configure the crawling hustle.

    This is where the magic happens - we connect three Jobs into a workflow:
        crawl >> analyze >> report

    Each Job passes data through the manifest, creating a pipeline that:
    1. Crawls websites
    2. Analyzes content in batches
    3. Generates a final report
    """
    # Create jobs
    crawl = CrawlWebsiteJob()
    analyze = AnalyzeContentJob()
    report = GenerateReportJob()

    # Connect jobs using the >> operator
    crawl >> analyze >> report

    # Create hustle
    return ct.Hustle(start=crawl)


if __name__ == "__main__":
    print("=" * 60)
    print("WEB CRAWLER WORKFLOW")
    print("=" * 60)
    print()
    print("This example demonstrates multi-stage workflow composition:")
    print("  1. CrawlWebsiteJob - Extract content from URLs")
    print("  2. AnalyzeContentJob (BatchJob) - Process in batches")
    print("  3. GenerateReportJob - Create summary report")
    print()
    print("Connected with: crawl >> analyze >> report")
    print()
    print("CodeTrain Philosophy (inspired by PocketFlow):")
    print("  Complex workflows = simple Jobs + connections")
    print("  Each Job does one thing well")
    print("  The manifest carries state between stages")
    print("=" * 60)
    print()

    # Get website URL from user
    url = input("Enter website URL to crawl (e.g., https://example.com): ")
    if not url:
        print("Error: URL is required")
        exit(1)

    # Initialize manifest
    manifest = {
        "base_url": url,
        "max_pages": 5,  # Limit for demo
    }

    # Create and run hustle
    print("\nStarting web crawl...\n")
    crawler = create_crawler_hustle()
    crawler.run(manifest)

    print("\n" + "=" * 60)
    print("✓ Crawling complete!")
    print(f"Results stored in manifest:")
    print(f"  - ['crawl_results']: {len(manifest.get('crawl_results', []))} pages")
    print(
        f"  - ['analyzed_results']: {len(manifest.get('analyzed_results', []))} analyzed"
    )
    print(f"  - ['report']: Full analysis report")
    print("=" * 60)
    print()
    print("Key Takeaway:")
    print("Complex workflows are just simple Jobs connected together.")
    print("Each Job focuses on one task, and the Hustle orchestrates them.")
    print()
    print("Learn more: https://github.com/Speedykom/CodeTrain")
    print("Inspired by: https://github.com/The-Pocket/PocketFlow")
    print("=" * 60)
