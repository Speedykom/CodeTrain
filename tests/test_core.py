"""Tests for codetrain package."""

import unittest
import codetrain


class TestCore(unittest.TestCase):
    def test_hello(self):
        result = codetrain.hello()
        self.assertEqual(result, "Hello from CodeTrain!")

    def test_trainer(self):
        trainer = codetrain.Trainer()
        self.assertEqual(trainer.version, "0.1.0")
        self.assertEqual(trainer.train(), "Training started...")


if __name__ == "__main__":
    unittest.main()
