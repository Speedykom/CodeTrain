"""Example: E-commerce Order Fulfillment

This example shows an order processing workflow with conditional routing:
- Standard delivery vs Express delivery paths
- Each path has different processing steps
- Final completion job merges both branches

CodeTrain Philosophy:
---------------------
Inspired by PocketFlow (https://github.com/The-Pocket/PocketFlow), this example
demonstrates conditional routing - where the workflow branches based on data.

The Routing Pattern:
    verify >> prepare >> choose
                        ├─ "standard" >> standard_delivery >> complete
                        └─ "express" >> express_delivery >> complete

Key Insight:
- Jobs can have multiple outputs (next_jobs)
- The return value determines which path to take
- Conditional routing enables complex business logic
- Perfect for: approval workflows, A/B testing, feature flags

This demonstrates how CodeTrain handles real-world business logic
through simple, expressive routing.
"""

import codetrain as ct


class VerifyPayment(ct.Job):
    """First job: Check if payment is confirmed."""

    def receive_order(self, manifest):
        return manifest.get("payment_status")

    def prepare_order(self, payment_status):
        if payment_status == "confirmed":
            return "default"  # Continue to next job
        else:
            return "failed"

    def ship_order(self, manifest, payment_status, result):
        print(f"[VerifyPayment] Order {manifest['order_id']}: Payment verified ✓")
        return result


class PreparePackage(ct.Job):
    """Second job: Pack the items."""

    def receive_order(self, manifest):
        return manifest["items"]

    def prepare_order(self, items):
        return f"Package with {len(items)} items"

    def ship_order(self, manifest, items, result):
        print(f"[PreparePackage] Prepared {result}")
        manifest["package_ready"] = True
        return "default"


class ChooseDelivery(ct.Job):
    """Third job: Route based on delivery method.

    This is where conditional routing happens!
    The return value ('standard' or 'express') determines the path.
    """

    def receive_order(self, manifest):
        return manifest.get("delivery_method", "standard")

    def prepare_order(self, method):
        return method  # Returns 'standard' or 'express'

    def ship_order(self, manifest, method, result):
        print(f"[ChooseDelivery] Routing to {result} delivery channel")
        return result


class StandardDelivery(ct.Job):
    """Standard delivery route."""

    def receive_order(self, manifest):
        return manifest

    def prepare_order(self, order_data):
        return f"Standard delivery to {order_data.get('destination')} (2-3 days)"

    def ship_order(self, manifest, order_data, result):
        print(f"[StandardDelivery] {result}")
        return "default"


class ExpressDelivery(ct.Job):
    """Express delivery route."""

    def receive_order(self, manifest):
        return manifest

    def prepare_order(self, order_data):
        return f"Express delivery to {order_data.get('destination')} (same day)"

    def ship_order(self, manifest, order_data, result):
        print(f"[ExpressDelivery] {result}")
        return "default"


class CompleteOrder(ct.Job):
    """Final job: Mark order as complete.

    This job receives control from both delivery paths,
    demonstrating how branches merge back together.
    """

    def deliver(self, shipment):
        return "Order fulfilled successfully"

    def ship_order(self, manifest, _, result):
        print(f"[CompleteOrder] ✓ {result}")
        manifest["status"] = "completed"
        return "done"


# Build the delivery route
print("=" * 60)
print("E-COMMERCE ORDER FULFILLMENT")
print("=" * 60)
print()
print("This example demonstrates conditional routing:")
print("  verify >> prepare >> choose")
print("                      ├─ 'standard' >> standard_delivery >> complete")
print("                      └─ 'express' >> express_delivery >> complete")
print()
print("CodeTrain Philosophy (inspired by PocketFlow):")
print("  Jobs can have multiple outputs (next_jobs)")
print("  Return value determines which path to take")
print("  Perfect for: approval workflows, business logic, A/B tests")
print("=" * 60)
print()

# Create stops
verify = VerifyPayment()
prepare = PreparePackage()
choose = ChooseDelivery()
standard = StandardDelivery()
express = ExpressDelivery()
complete = CompleteOrder()

# Connect the route:
# Main flow: verify >> prepare >> choose
# Branching from choose: standard or express >> complete
verify >> prepare >> choose
choose - "standard" >> standard >> complete
choose - "express" >> express >> complete

# Create the route starting from verify
fulfillment_hustle = ct.Hustle(start=verify)

# Test with standard delivery
order = {
    "order_id": "ORD-001",
    "customer": "Ama Mensah",
    "items": ["phone", "charger"],
    "payment_status": "confirmed",
    "destination": "Accra, Ghana",
    "delivery_method": "standard",
}

print("TEST 1: Standard Delivery")
print("-" * 60)
print(f"Processing order: {order['order_id']}")
print(f"Customer: {order['customer']}")
print(f"Items: {', '.join(order['items'])}")
print(f"Delivery: {order['delivery_method']}")
print("-" * 60)

result = fulfillment_hustle.run(order)

print("-" * 60)
print(f"Final action: {result}")
print(f"Order status: {order.get('status')}")
print(f"Package ready: {order.get('package_ready')}")

# Test with express delivery
print("\n" + "=" * 60)
print("TEST 2: Express Delivery")
print("=" * 60)

express_order = {
    "order_id": "ORD-002",
    "customer": "Kwame Asante",
    "items": ["laptop", "mouse"],
    "payment_status": "confirmed",
    "destination": "Kumasi, Ghana",
    "delivery_method": "express",
}

print(f"Processing order: {express_order['order_id']}")
print(f"Customer: {express_order['customer']}")
print(f"Delivery: {express_order['delivery_method']}")
print("-" * 60)

result2 = fulfillment_hustle.run(express_order)

print("-" * 60)
print(f"Final action: {result2}")
print(f"Order status: {express_order.get('status')}")

# Example 3: Batch processing with BatchJob
print("\n" + "=" * 60)
print("TEST 3: Batch Processing (BatchJob)")
print("=" * 60)


class PrintLabel(ct.BatchJob):
    """Print shipping label for each order in a batch.

    MultiDrop automatically iterates over a list and calls deliver()
    for each item individually.
    """

    def load(self, cargo):
        # Must return the list to iterate over
        return cargo

    def deliver(self, order):
        # This is called once per order
        label = f"Label-{order['order_id']}"
        print(f"  Printed {label} for {order['customer']}")
        return label


orders = [
    {"order_id": "ORD-003", "customer": "Abena", "items": ["shoes"]},
    {"order_id": "ORD-004", "customer": "Kofi", "items": ["book", "pen"]},
    {"order_id": "ORD-005", "customer": "Yaa", "items": ["headphones"]},
]

print(f"\nBatch processing {len(orders)} orders:")
print("-" * 60)

# For MultiDrop, we pass the list of orders directly
# The load() method returns the list
# MultiDrop then iterates and calls deliver() for each order
label_printer = PrintLabel()
results = label_printer.run(orders)

print("-" * 60)
print(f"Results: {results}")

print("\n" + "=" * 60)
print("Key Takeaway:")
print("Conditional routing lets you build complex business logic:")
print("  job - 'action1' >> path_a")
print("  job - 'action2' >> path_b")
print("The Job's return value determines which path is taken.")
print("Both paths can merge back to a common endpoint.")
print()
print("Learn more: https://github.com/Speedykom/CodeTrain")
print("Inspired by: https://github.com/The-Pocket/PocketFlow")
print("=" * 60)
