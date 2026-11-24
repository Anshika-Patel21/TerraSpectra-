
import unittest
import numpy as np

from app.services.model_adapter import MockModelAdapter


class TestModelAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = MockModelAdapter()

    def test_model_load(self):
        self.adapter.load()

    def test_mock_prediction(self):
        tile = np.ones((10, 10, 3), dtype=np.float32)

        result = self.adapter.predict(tile)

        self.assertEqual(result["risk_class"], "Medium")
        self.assertEqual(result["prediction_type"], "mock")
        self.assertEqual(result["score"], 0.55)

    def test_empty_tile(self):
        with self.assertRaises(ValueError):
            self.adapter.predict(np.array([]))


if __name__ == "__main__":
    unittest.main()
