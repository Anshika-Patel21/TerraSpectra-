
import numpy as np
import tensorflow as tf

from pathlib import Path
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# ==========================================
# PROJECT CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
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


# ==========================================
# GRAPEVINE DISEASE PREDICTOR
# ==========================================

class GrapevineDiseasePredictor:

    def __init__(self, model_path=MODEL_PATH):

        model_path = Path(model_path)

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        self.model = tf.keras.models.load_model(
            model_path,
            compile=False
        )

        print(
            "TerraSpectra MobileNetV2 model loaded successfully!"
        )

    # ======================================
    # IMAGE PREPROCESSING
    # ======================================

    def preprocess_image(self, image_path):

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        # Read image using TensorFlow
        image = tf.io.read_file(
            str(image_path)
        )

        image = tf.io.decode_image(
            image,
            channels=3,
            expand_animations=False
        )

        image.set_shape([None, None, 3])

        # Resize exactly as in training pipeline
        image = tf.image.resize(
            image,
            IMG_SIZE
        )

        image = tf.cast(
            image,
            tf.float32
        )

        # MobileNetV2 preprocessing: [-1, 1]
        image = preprocess_input(image)

        # Add batch dimension
        image = tf.expand_dims(
            image,
            axis=0
        )

        return image

    # ======================================
    # DISEASE PREDICTION
    # ======================================

    def predict(self, image_path):

        image = self.preprocess_image(
            image_path
        )

        probabilities = self.model.predict(
            image,
            verbose=0
        )[0]

        predicted_index = int(
            np.argmax(probabilities)
        )

        predicted_disease = CLASS_NAMES[
            predicted_index
        ]

        confidence = float(
            probabilities[predicted_index]
        )

        result = {
            "predicted_disease": predicted_disease,

            "confidence": round(
                confidence, 4
            ),

            "probabilities": {
                class_name: round(
                    float(probability), 4
                )
                for class_name, probability
                in zip(CLASS_NAMES, probabilities)
            }
        }

        return result


# ==========================================
# LOCAL TEST
# ==========================================

if __name__ == "__main__":

    predictor = GrapevineDiseasePredictor()

    print(
        "TerraSpectra inference module initialized successfully."
    )
