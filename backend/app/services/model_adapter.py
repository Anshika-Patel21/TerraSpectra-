
from typing import Any, Protocol

import numpy as np


class ModelAdapter(Protocol):
    """Interface for connecting ML models to the backend."""

    def load(self) -> None:
        """Load model weights or checkpoint."""
        ...

    def predict(self, tile: np.ndarray) -> dict[str, Any]:
        """Run inference on one raster tile."""
        ...


class MockModelAdapter:
    """Temporary adapter for backend integration testing."""

    def load(self) -> None:
        pass

    def predict(self, tile: np.ndarray) -> dict[str, Any]:
        if tile.size == 0:
            raise ValueError("Input tile cannot be empty")

        return {
            "risk_class": "Medium",
            "score": 0.55,
            "prediction_type": "mock"
        }

