
"""
TerraSpectra - RGB 3D-CNN Image Inference

Usage:
python src/inference_3dcnn.py "path/to/leaf_image.jpg"
"""

import sys
from pathlib import Path

import numpy as np
import tensorflow as tf


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "terraspectra_rgb_3dcnn_best.keras"
)

IMAGE_SIZE = 64

CLASS_NAMES = [
    "Black rot",
    "Esca",
    "Healthy",
    "Leaf blight"
]


# --------------------------------------------------
# Load model
# --------------------------------------------------

def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    print("Loading RGB 3D-CNN model...")

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print("Model loaded successfully.")

    return model


# --------------------------------------------------
# Preprocess image
# Must match training preprocessing
# --------------------------------------------------

def preprocess_image(image_path):

    image_bytes = tf.io.read_file(
        str(image_path)
    )

    image = tf.io.decode_jpeg(
        image_bytes,
        channels=3
    )

    image = tf.image.resize(
        image,
        [IMAGE_SIZE, IMAGE_SIZE]
    )

    image = tf.cast(
        image,
        tf.float32
    ) / 255.0

    # (64, 64, 3) -> (3, 64, 64)
    image = tf.transpose(
        image,
        perm=[2, 0, 1]
    )

    # Add channel dimension
    # (3, 64, 64) -> (3, 64, 64, 1)
    image = tf.expand_dims(
        image,
        axis=-1
    )

    # Add batch dimension
    # (3, 64, 64, 1) -> (1, 3, 64, 64, 1)
    image = tf.expand_dims(
        image,
        axis=0
    )

    return image


# --------------------------------------------------
# Predict disease
# --------------------------------------------------

def predict_image(model, image_path):

    image = preprocess_image(
        image_path
    )

    probabilities = model.predict(
        image,
        verbose=0
    )[0]

    predicted_index = int(
        np.argmax(probabilities)
    )

    predicted_class = CLASS_NAMES[
        predicted_index
    ]

    confidence = float(
        probabilities[predicted_index]
    ) * 100

    print("\n" + "=" * 50)
    print("TERRASPECTRA GRAPEVINE DISEASE PREDICTION")
    print("=" * 50)

    print(f"\nImage: {image_path.name}")

    print(
        f"\nPredicted Disease: {predicted_class}"
    )

    print(
        f"Confidence: {confidence:.2f}%"
    )

    print("\nClass-wise probabilities:")

    for index, class_name in enumerate(CLASS_NAMES):

        probability = (
            float(probabilities[index]) * 100
        )

        print(
            f"{class_name:<15}: {probability:.2f}%"
        )

    print("\n" + "=" * 50)

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "probabilities": probabilities.tolist()
    }


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    if len(sys.argv) < 2:

        print(
            "\nUsage:"
            '\npython src/inference_3dcnn.py "path/to/image.jpg"'
        )

        return

    image_path = Path(
        sys.argv[1]
    ).resolve()

    if not image_path.exists():

        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    model = load_model()

    predict_image(
        model,
        image_path
    )


if __name__ == "__main__":

    main()
