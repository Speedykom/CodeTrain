"""Tests for codetrain logistics workflow engine."""

import unittest
import codetrain as ct


class TestJob(unittest.TestCase):
    def test_job_execution(self):
        """Test basic job execution."""

        class TestJob(ct.Job):
            def prepare_order(self, data):
                return f"processed {data}"

            def ship_order(self, manifest, data, result):
                return result

        job = TestJob()
        manifest = {}
        result = job.run(manifest)
        self.assertEqual(result, "processed None")

    def test_job_with_data(self):
        """Test job with receive_order."""

        class TestJob(ct.Job):
            def receive_order(self, manifest):
                return manifest.get("value")

            def prepare_order(self, data):
                return data * 2

            def ship_order(self, manifest, data, result):
                return result

        job = TestJob()
        manifest = {"value": 21}
        result = job.run(manifest)
        self.assertEqual(result, 42)


class TestHustle(unittest.TestCase):
    def test_hustle_chain(self):
        """Test chaining jobs in a hustle."""

        class Step1(ct.Job):
            def prepare_order(self, _):
                return "step1_done"

            def ship_order(self, manifest, _, result):
                manifest["step1"] = result
                return "next"

        class Step2(ct.Job):
            def prepare_order(self, _):
                return "step2_done"

            def ship_order(self, manifest, _, result):
                manifest["step2"] = result
                return "done"

        step1 = Step1()
        step2 = Step2()
        step1 - "next" >> step2

        hustle = ct.Hustle(start=step1)
        manifest = {}
        result = hustle.run(manifest)

        self.assertEqual(result, "done")
        self.assertEqual(manifest["step1"], "step1_done")
        self.assertEqual(manifest["step2"], "step2_done")

    def test_conditional_routing(self):
        """Test conditional job routing."""

        class Router(ct.Job):
            def receive_order(self, manifest):
                return manifest.get("route")

            def prepare_order(self, route):
                return route

            def ship_order(self, manifest, route, result):
                return result

        class PathA(ct.Job):
            def prepare_order(self, _):
                return "path_a"

            def ship_order(self, m, _, r):
                m["taken"] = r
                return "done"

        class PathB(ct.Job):
            def prepare_order(self, _):
                return "path_b"

            def ship_order(self, m, _, r):
                m["taken"] = r
                return "done"

        router = Router()
        path_a = PathA()
        path_b = PathB()

        router - "a" >> path_a
        router - "b" >> path_b

        # Test route A
        hustle = ct.Hustle(start=router)
        manifest_a = {"route": "a"}
        hustle.run(manifest_a)
        self.assertEqual(manifest_a["taken"], "path_a")

        # Test route B
        manifest_b = {"route": "b"}
        hustle.run(manifest_b)
        self.assertEqual(manifest_b["taken"], "path_b")


class TestBatchJob(unittest.TestCase):
    def test_batch_processing(self):
        """Test batch job processes multiple items."""

        class Doubler(ct.BatchJob):
            def receive_order(self, manifest):
                return manifest

            def prepare_order(self, num):
                return num * 2

            def ship_order(self, manifest, data, results):
                return results

        batch = Doubler()
        manifest = [1, 2, 3, 4, 5]
        results = batch.run(manifest)

        self.assertEqual(results, [2, 4, 6, 8, 10])


class TestRetry(unittest.TestCase):
    def test_job_retry(self):
        """Test job retries on failure."""

        attempts = []

        class FailingJob(ct.Job):
            def __init__(self):
                super().__init__(max_retries=3, wait=0)

            def prepare_order(self, _):
                attempts.append(len(attempts) + 1)
                if len(attempts) < 3:
                    raise ValueError("Not yet")
                return "success"

            def ship_order(self, m, _, r):
                return r

        job = FailingJob()
        result = job.run({})

        self.assertEqual(result, "success")
        self.assertEqual(len(attempts), 3)


class TestLegacyAliases(unittest.TestCase):
    """Test that legacy aliases still work."""

    def test_stop_alias(self):
        """Test that Stop is an alias for Job."""
        self.assertIs(ct.Stop, ct.Job)

    def test_route_alias(self):
        """Test that Route is an alias for Hustle."""
        self.assertIs(ct.Route, ct.Hustle)

    def test_multidrop_alias(self):
        """Test that MultiDrop is an alias for BatchJob."""
        self.assertIs(ct.MultiDrop, ct.BatchJob)


if __name__ == "__main__":
    unittest.main()
