from pathlib import Path
from typing import Any, Protocol

import numpy as np


MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "terraspectra_mobilenetv2_final.keras"
)

IMG_SIZE = (224, 224)

CLASS_NAMES = [
    "Black rot",
    "Esca",
    "Healthy",
    "Leaf blight"
]


class ModelAdapter(Protocol):
    def load(self) -> None:
        ...

    def predict(self, image_path: str) -> dict[str, Any]:
        ...


class RealModelAdapter:
    """Adapter for the trained TerraSpectra MobileNetV2 model."""

    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = Path(model_path)
        self.model = None

    def load(self) -> None:
        import tensorflow as tf

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        self.model = tf.keras.models.load_model(
            self.model_path,
            compile=False
        )

    def predict(self, image_path: str) -> dict[str, Any]:
        import tensorflow as tf
        from tensorflow.keras.applications.mobilenet_v2 import (
            preprocess_input
        )

        if self.model is None:
            self.load()

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image = tf.io.read_file(str(image_path))
        image = tf.io.decode_image(
            image,
            channels=3,
            expand_animations=False
        )

        image.set_shape([None, None, 3])
        image = tf.image.resize(image, IMG_SIZE)
        image = tf.cast(image, tf.float32)
        image = preprocess_input(image)
        image = tf.expand_dims(image, axis=0)

        probabilities = self.model.predict(
            image,
            verbose=0
        )[0]

        if len(probabilities) != len(CLASS_NAMES):
            raise ValueError("Unexpected model output dimensions")

        predicted_index = int(np.argmax(probabilities))

        return {
            "predicted_disease": CLASS_NAMES[predicted_index],
            "confidence": round(
                float(probabilities[predicted_index]), 4
            ),
            "probabilities": {
                name: round(float(score), 4)
                for name, score in zip(
                    CLASS_NAMES, probabilities
                )
            },
            "prediction_type": "trained_model",
            "status": "success"
        }
class MockModelAdapter:
    """Temporary adapter for backend integration testing."""

    def load(self) -> None:
        pass

    def predict(self, tile: np.ndarray) -> dict[str, Any]:
        if tile.size == 0:
            raise ValueError("Tile cannot be empty")

        return {
            "risk_class": "Medium",
            "score": 0.55,
            "prediction_type": "mock"
        }


