"""Example 5: Data Processing Pipeline

This example shows a multi-stage data processing workflow:
1. Load data from source
2. Clean and validate data
3. Transform data
4. Save results

CodeTrain Philosophy:
---------------------
Following PocketFlow's minimalist approach (https://github.com/The-Pocket/PocketFlow),
we break a complex data pipeline into simple, composable Jobs.

The Pipeline Pattern:
    load >> clean >> transform >> report

Each Job:
- Does one thing well
- Receives data from the previous Job via manifest
- Stores results back in the manifest
- Passes control to the next Job

Key Insight:
- Data pipelines are just sequential Jobs
- Error handling at each stage
- Data quality improves stage by stage
- Final report summarizes the entire process

This demonstrates how CodeTrain brings clarity to complex workflows
through simple, focused Jobs.
"""

import codetrain as ct


class LoadDataJob(ct.Job):
    """Load raw data from a source.

    Stage 1: Ingestion
    - Receive configuration from manifest
    - Load data from source (file, API, database, etc.)
    - Store raw data in manifest for next stage
    """

    def receive_order(self, manifest):
        """Get data source from manifest."""
        source = manifest.get("data_source", "mock")

        if source == "mock":
            # Generate mock sales data
            return [
                {"id": 1, "product": "Laptop", "price": "1200.00", "quantity": "2"},
                {"id": 2, "product": "Mouse", "price": "25.50", "quantity": "5"},
                {"id": 3, "product": "Keyboard", "price": "invalid", "quantity": "3"},
                {
                    "id": 4,
                    "product": "Monitor",
                    "price": "300.00",
                    "quantity": "invalid",
                },
                {"id": 5, "product": "USB Cable", "price": "15.00", "quantity": "10"},
            ]

        return manifest.get("raw_data", [])

    def prepare_order(self, data):
        """Pass data through."""
        return data

    def ship_order(self, manifest, _, raw_data):
        """Store raw data."""
        manifest["raw_data"] = raw_data
        print(f"✓ Loaded {len(raw_data)} records")
        return "default"


class CleanDataJob(ct.Job):
    """Clean and validate data.

    Stage 2: Cleaning
    - Receive raw data from manifest
    - Validate and convert data types
    - Handle errors gracefully
    - Store clean data and errors separately
    """

    def receive_order(self, manifest):
        """Get raw data."""
        return manifest.get("raw_data", [])

    def prepare_order(self, raw_data):
        """Clean and validate each record."""
        cleaned = []
        errors = []

        for record in raw_data:
            try:
                # Try to convert price and quantity to numbers
                price = float(record.get("price", 0))
                quantity = int(record.get("quantity", 0))

                cleaned.append(
                    {
                        "id": record["id"],
                        "product": record["product"].strip(),
                        "price": price,
                        "quantity": quantity,
                        "total": price * quantity,
                    }
                )
            except (ValueError, TypeError) as e:
                errors.append({"record": record, "error": str(e)})

        return {"cleaned": cleaned, "errors": errors}

    def ship_order(self, manifest, _, result):
        """Store cleaned data and errors."""
        manifest["cleaned_data"] = result["cleaned"]
        manifest["errors"] = result["errors"]

        print(f"✓ Cleaned {len(result['cleaned'])} records")
        if result["errors"]:
            print(f"✗ Found {len(result['errors'])} errors")
            for err in result["errors"]:
                print(f"   - Record {err['record'].get('id')}: {err['error']}")

        return "default"


class TransformDataJob(ct.Job):
    """Transform data into useful formats.

    Stage 3: Transformation
    - Receive cleaned data from manifest
    - Calculate aggregates and metrics
    - Generate insights
    - Store metrics for reporting
    """

    def receive_order(self, manifest):
        """Get cleaned data."""
        return manifest.get("cleaned_data", [])

    def prepare_order(self, cleaned_data):
        """Calculate aggregates and metrics."""
        if not cleaned_data:
            return {}

        # Calculate totals
        total_revenue = sum(item["total"] for item in cleaned_data)
        total_items = sum(item["quantity"] for item in cleaned_data)

        # Group by product
        product_summary = {}
        for item in cleaned_data:
            product = item["product"]
            if product not in product_summary:
                product_summary[product] = {"count": 0, "revenue": 0}
            product_summary[product]["count"] += item["quantity"]
            product_summary[product]["revenue"] += item["total"]

        return {
            "total_revenue": total_revenue,
            "total_items": total_items,
            "record_count": len(cleaned_data),
            "product_summary": product_summary,
        }

    def ship_order(self, manifest, _, metrics):
        """Store metrics."""
        manifest["metrics"] = metrics
        print(f"✓ Calculated metrics for {metrics.get('record_count', 0)} records")
        return "default"


class GenerateReportJob(ct.Job):
    """Generate final report.

    Stage 4: Reporting
    - Receive all data from manifest
    - Format into readable report
    - Display and store results
    """

    def receive_order(self, manifest):
        """Get all data."""
        return {
            "metrics": manifest.get("metrics", {}),
            "errors": manifest.get("errors", []),
        }

    def prepare_order(self, data):
        """Generate report."""
        metrics = data["metrics"]
        errors = data["errors"]

        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("DATA PROCESSING REPORT")
        report_lines.append("=" * 60)

        report_lines.append(f"\n📊 Summary:")
        report_lines.append(f"   Records processed: {metrics.get('record_count', 0)}")
        report_lines.append(
            f"   Total revenue: ${metrics.get('total_revenue', 0):,.2f}"
        )
        report_lines.append(f"   Total items: {metrics.get('total_items', 0)}")
        report_lines.append(f"   Errors: {len(errors)}")

        if metrics.get("product_summary"):
            report_lines.append(f"\n📦 Product Breakdown:")
            for product, stats in metrics["product_summary"].items():
                report_lines.append(
                    f"   {product:15} | Qty: {stats['count']:3} | Revenue: ${stats['revenue']:>10,.2f}"
                )

        if errors:
            report_lines.append(f"\n⚠️  Errors:")
            for err in errors:
                report_lines.append(f"   - {err['record']}")

        report_lines.append("\n" + "=" * 60)

        return "\n".join(report_lines)

    def ship_order(self, manifest, _, report):
        """Store and display report."""
        manifest["report"] = report
        print("\n" + report)
        return "done"


if __name__ == "__main__":
    print("=" * 60)
    print("DATA PROCESSING PIPELINE")
    print("=" * 60)
    print()
    print("This example demonstrates a 4-stage data pipeline:")
    print("  1. LoadDataJob     - Ingest raw data")
    print("  2. CleanDataJob    - Validate and clean")
    print("  3. TransformDataJob - Calculate metrics")
    print("  4. GenerateReportJob - Create summary")
    print()
    print("Connected with: load >> clean >> transform >> report")
    print()
    print("CodeTrain Philosophy (inspired by PocketFlow):")
    print("  Complex pipelines = simple Jobs + clear connections")
    print("  Each stage focuses on one transformation")
    print("  Data quality improves progressively")
    print("  Final report summarizes everything")
    print("=" * 60)
    print()

    # Create jobs
    load = LoadDataJob()
    clean = CleanDataJob()
    transform = TransformDataJob()
    report = GenerateReportJob()

    # Connect them
    load >> clean >> transform >> report

    # Create hustle
    pipeline = ct.Hustle(start=load)

    # Initialize manifest
    manifest = {"data_source": "mock"}

    # Run the pipeline
    print("Starting pipeline...\n")
    pipeline.run(manifest)

    print("\n" + "=" * 60)
    print("✓ Pipeline complete!")
    print(f"  - Records loaded: {len(manifest.get('raw_data', []))}")
    print(f"  - Records cleaned: {len(manifest.get('cleaned_data', []))}")
    print(f"  - Errors found: {len(manifest.get('errors', []))}")
    print(
        f"  - Total revenue: ${manifest.get('metrics', {}).get('total_revenue', 0):,.2f}"
    )
    print("=" * 60)
    print()
    print("Key Takeaway:")
    print("Data pipelines are just sequential Jobs connected with >>.")
    print("Each Job does one transformation, passing improved data")
    print("through the manifest to the next stage.")
    print()
    print("Learn more: https://github.com/Speedykom/CodeTrain")
    print("Inspired by: https://github.com/The-Pocket/PocketFlow")
    print("=" * 60)
