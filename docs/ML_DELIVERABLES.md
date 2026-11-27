
# TerraSpectra – RGB Grapevine Disease Classification: Model Documentation

## 1. Project Overview

TerraSpectra is a deep learning project developed to classify grapevine leaf diseases using image-based machine learning techniques.

The project uses RGB images of grapevine leaves and compares three deep learning architectures:

1. MobileNetV2 – Transfer learning baseline.
2. RGB 3D-CNN – Experimental 3D convolutional neural network.
3. DeiT-Tiny – Lightweight Vision Transformer comparison.

The objective is to classify grapevine leaf images into four categories:

- Black rot
- Esca
- Healthy
- Leaf blight

The models are evaluated using accuracy, precision, recall, F1-score and confusion matrices.

**Dataset clarification:** The current dataset contains conventional RGB JPEG images. It is not a hyperspectral dataset. The 3D-CNN experiment rearranges the three RGB channels into a depth dimension, but these channels are not independent spectral bands or wavelength measurements.

---

## 2. Dataset Description

### 2.1 Dataset Information

| Property | Description |
|---|---|
| Dataset | GVLiD grapevine leaf image dataset |
| Image format | JPEG |
| Original image resolution | 1080 × 1080 |
| Image type | RGB |
| Number of images | 3,477 |
| Number of classes | 4 |
| Train split | 1,730 images |
| Validation split | 341 images |
| Test split | 336 images |
| Total split records | 2,407 images |

The existing final split files contain 2,407 records. Therefore, the total number of original dataset images should not be confused with the number of images represented in the final train, validation and test splits.

### 2.2 Class Labels

| Class ID | Disease Category |
|---|---|
| 0 | Black rot |
| 1 | Esca |
| 2 | Healthy |
| 3 | Leaf blight |

### 2.3 Dataset Distribution

The training split contains the following class distribution:

| Class | Training Images |
|---|---:|
| Black rot | 72 |
| Esca | 635 |
| Healthy | 788 |
| Leaf blight | 235 |
| **Total** | **1,730** |

The dataset is imbalanced because the number of images available for each disease category is different.

Class imbalance can affect model performance, particularly for classes with fewer training examples.

---

## 3. Data Preprocessing Pipeline

Preprocessing converts the original images into a consistent format suitable for deep learning models.

The project uses model-specific preprocessing because each architecture expects a different input representation.

### 3.1 Common Preprocessing

The general preprocessing steps include:

1. Reading image paths from the dataset CSV files.
2. Loading images from their original JPEG files.
3. Converting images into RGB format.
4. Resizing images according to the model requirements.
5. Converting pixel values into numerical tensors.
6. Normalizing image values where required.
7. Assigning numerical class labels.
8. Preparing training, validation and test datasets.

### 3.2 MobileNetV2 Preprocessing

MobileNetV2 uses conventional RGB image input.

| Property | Value |
|---|---|
| Image format | RGB |
| Input resolution | 224 × 224 |
| Number of channels | 3 |
| Input shape | 224 × 224 × 3 |

The images are resized and prepared according to the MobileNetV2 input requirements.

### 3.3 RGB 3D-CNN Preprocessing

The experimental 3D-CNN uses a different representation.

Preprocessing steps:

1. Load the RGB image.
2. Resize the image to 64 × 64 pixels.
3. Normalize pixel values to the range 0–1.
4. Convert the image into a NumPy tensor.
5. Rearrange the RGB channel dimension into a depth dimension.
6. Add a final channel dimension for Conv3D processing.

Original image shape:

`(64, 64, 3)`

After rearranging the dimensions:

`(3, 64, 64)`

Final model input shape:

`(3, 64, 64, 1)`

**Important clarification:** The depth dimension represents the three RGB channels. It does not represent actual hyperspectral bands, wavelengths or spectral measurements.

### 3.4 DeiT-Tiny Preprocessing

DeiT-Tiny uses an ImageNet-compatible image processor.

| Property | Value |
|---|---|
| Image format | RGB |
| Input resolution | 224 × 224 |
| Number of channels | 3 |
| Individual image tensor | 3 × 224 × 224 |
| Model | facebook/deit-tiny-patch16-224 |

The pretrained image processor handles resizing, normalization and conversion into the tensor format expected by the transformer.

---

## 4. Model 1: MobileNetV2 Baseline

### 4.1 Introduction

MobileNetV2 is a lightweight convolutional neural network architecture designed for efficient image classification.

It uses depthwise separable convolutions and inverted residual blocks to reduce computational requirements.

MobileNetV2 was used as the baseline model for grapevine disease classification.

### 4.2 Main Characteristics

- Pretrained convolutional neural network.
- Transfer learning approach.
- RGB image input.
- Four-class classification.
- Lightweight architecture.
- Suitable as a comparison baseline.

### 4.3 Evaluation Results

The model was evaluated using the final test dataset containing 336 images.

| Metric | Result |
|---|---:|
| Test Accuracy | 83.93% |
| Macro F1-score | 0.7610 |
| Weighted F1-score | 0.8433 |

### 4.4 Per-Class F1-score

| Class | F1-score | Test Support |
|---|---:|---:|
| Black rot | 0.73 | 11 |
| Esca | 0.80 | 126 |
| Healthy | 0.99 | 150 |
| Leaf blight | 0.52 | 49 |

The baseline model performs particularly well for healthy leaves. However, performance is comparatively weaker for leaf blight.

### 4.5 Model Checkpoint

`models/terraspectra_mobilenetv2_final.keras`

---

## 5. Model 2: RGB 3D-CNN

### 5.1 Introduction

A 3D Convolutional Neural Network (3D-CNN) was developed as an experimental architecture for grapevine disease classification.

Unlike a conventional 2D-CNN, which applies convolution operations across image height and width, a 3D-CNN applies convolution operations across three dimensions.

In this experiment, the three RGB channels are arranged along the depth dimension.

This experiment explores a 3D convolutional architecture using RGB images. It should not be interpreted as a true hyperspectral deep learning model.

### 5.2 Model Architecture

The RGB 3D-CNN contains the following layers:

1. Input layer.
2. 3D Convolution layer with 8 filters.
3. 3D Max Pooling layer.
4. Batch Normalization.
5. 3D Convolution layer with 16 filters.
6. 3D Max Pooling layer.
7. Batch Normalization.
8. 3D Convolution layer with 32 filters.
9. Global Average Pooling.
10. Dropout layer with a rate of 0.35.
11. Dense output layer with 4 units.
12. Softmax activation.

### 5.3 Training Configuration

| Parameter | Value |
|---|---|
| Input image size | 64 × 64 |
| Input tensor shape | 3 × 64 × 64 × 1 |
| Batch size | 4 |
| Epochs | 15 |
| Optimizer | Adam |
| Learning rate | 0.001 |
| Loss function | Sparse Categorical Crossentropy |
| Number of classes | 4 |
| Random seed | 42 |

The training process also uses:

- ModelCheckpoint to save the best model.
- EarlyStopping to reduce unnecessary training.
- ReduceLROnPlateau to adjust the learning rate when validation performance stops improving.

### 5.4 Evaluation Results

The model was evaluated on the same test split containing 336 images.

| Metric | Result |
|---|---:|
| Test Images | 336 |
| Correct Predictions | 296 |
| Incorrect Predictions | 40 |
| Test Accuracy | 88.10% |
| Macro Precision | 0.8037 |
| Macro Recall | 0.7890 |
| Macro F1-score | 0.7834 |
| Weighted F1-score | 0.8706 |

### 5.5 Per-Class Evaluation

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Black rot | 0.69 | 0.82 | 0.75 | 11 |
| Esca | 0.81 | 0.94 | 0.87 | 126 |
| Healthy | 1.00 | 0.99 | 1.00 | 150 |
| Leaf blight | 0.71 | 0.41 | 0.52 | 49 |

### 5.6 Interpretation

The RGB 3D-CNN achieved the highest test accuracy among the three evaluated models.

It performed particularly well for Esca and Healthy categories.

However, its recall for Leaf blight is comparatively low. This indicates that the model misses a proportion of actual leaf blight samples.

The result should be treated as preliminary because the dataset is relatively small and imbalanced.

### 5.7 Model Checkpoint

`models/terraspectra_rgb_3dcnn_best.keras`

---

## 6. Model 3: DeiT-Tiny Vision Transformer

### 6.1 Introduction

Data-efficient Image Transformers (DeiT) are Vision Transformer architectures designed for image classification.

Unlike conventional CNN architectures, Vision Transformers divide an image into smaller patches and use self-attention mechanisms to learn relationships between different image regions.

The project uses the pretrained DeiT-Tiny model from Hugging Face.

**Pretrained model:** `facebook/deit-tiny-patch16-224`

### 6.2 Model Configuration

| Parameter | Value |
|---|---|
| Architecture | DeiT-Tiny |
| Pretrained weights | ImageNet-1K |
| Input resolution | 224 × 224 |
| Image channels | 3 |
| Number of output classes | 4 |
| Training approach | Linear probing |
| Hardware | CPU |
| Batch size | 8 |
| Epochs | 12 |
| Optimizer | AdamW |
| Learning rate | 0.0005 |
| Loss function | Cross Entropy Loss |

### 6.3 Transfer Learning Approach

The pretrained DeiT-Tiny backbone is used as a feature extractor.

The pretrained backbone parameters are frozen, and the final classification head is adapted to classify the four grapevine categories.

This approach is known as linear probing.

Class weights are used during training to help address the imbalance in the training dataset.

### 6.4 Validation Results

The best checkpoint was selected using validation loss.

| Metric | Result |
|---|---:|
| Best Epoch | 12 |
| Best Validation Loss | 0.3940 |
| Validation Accuracy | 83.87% |
| Macro F1-score | 0.7880 |
| Weighted F1-score | 0.8394 |

### 6.5 Test Evaluation Results

The model was evaluated on the independent test dataset containing 336 images.

| Metric | Result |
|---|---:|
| Test Images | 336 |
| Correct Predictions | 273 |
| Incorrect Predictions | 63 |
| Test Accuracy | 81.25% |
| Macro Precision | 0.6952 |
| Macro Recall | 0.7005 |
| Macro F1-score | 0.6970 |
| Weighted F1-score | 0.8146 |

### 6.6 Per-Class Evaluation

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Black rot | 0.55 | 0.55 | 0.55 | 11 |
| Esca | 0.81 | 0.75 | 0.78 | 126 |
| Healthy | 0.96 | 0.98 | 0.97 | 150 |
| Leaf blight | 0.46 | 0.53 | 0.50 | 49 |

### 6.7 Interpretation

DeiT-Tiny achieved 81.25% accuracy on the test dataset.

It performed well for the Healthy category but showed comparatively weaker results for Black rot and Leaf blight.

The experiment demonstrates the use of a lightweight pretrained Vision Transformer for grapevine disease classification.

However, it did not outperform the RGB 3D-CNN or MobileNetV2 on the current test split.

---

## 7. Overall Model Comparison

All three models were evaluated using the same test split containing 336 images.

| Model | Test Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| MobileNetV2 | 83.93% | 0.7610 | 0.8433 |
| RGB 3D-CNN | 88.10% | 0.7834 | 0.8706 |
| DeiT-Tiny | 81.25% | 0.6970 | 0.8146 |

### 7.1 Comparison and Findings

Based on the current test results:

1. RGB 3D-CNN achieved the highest test accuracy of 88.10%.
2. RGB 3D-CNN also achieved the highest macro F1-score of 0.7834.
3. MobileNetV2 achieved 83.93% test accuracy and provides a useful baseline.
4. DeiT-Tiny achieved 81.25% test accuracy.
5. All three models performed well for the Healthy category.
6. Leaf blight remains a challenging category across the evaluated architectures.

### 7.2 Selected Model

The RGB 3D-CNN is the best-performing model among the three evaluated architectures based on the current test results.

However, this result does not establish that the architecture will generalize better to images from different vineyards, cameras, lighting conditions or geographical regions.

Additional external validation is required before selecting it for real-world deployment.

---

## 8. Model Outputs and Prediction Scores

All three models classify an input image into one of four grapevine categories.

The model produces scores for the four output classes.

For models using a softmax output layer, these scores are normalized to sum to approximately 1.

### 8.1 Output Classes

| Class ID | Output Class |
|---|---|
| 0 | Black rot |
| 1 | Esca |
| 2 | Healthy |
| 3 | Leaf blight |

### 8.2 Prediction Confidence

The predicted class is selected using the highest output score.

For example:

| Class | Example Score |
|---|---:|
| Black rot | 0.02 |
| Esca | 0.03 |
| Healthy | 0.94 |
| Leaf blight | 0.01 |

Predicted class: Healthy

Confidence score: 94%

The confidence score represents the model's highest output probability. It should not be interpreted as a guarantee that the prediction is correct or as a clinically calibrated probability.

### 8.3 Inference

The RGB 3D-CNN inference script can be executed using:

`python src/inference_3dcnn.py "path/to/leaf_image.jpg"`

The inference process:

1. Loads the trained checkpoint.
2. Reads the input image.
3. Applies the required preprocessing.
4. Generates class scores.
5. Selects the class with the highest score.
6. Displays the predicted disease and confidence.

The existing MobileNetV2 inference implementation uses the `GrapevineDiseasePredictor` class and provides the predicted disease, confidence and class probabilities.

---

## 9. Evaluation Metrics and Reports

The project uses multiple evaluation metrics to assess classification performance.

### 9.1 Accuracy

Accuracy measures the proportion of correctly classified images.

Accuracy = Correct Predictions / Total Predictions

### 9.2 Precision

Precision measures how many images predicted as a particular class actually belong to that class.

Precision = TP / (TP + FP)

### 9.3 Recall

Recall measures how many actual images belonging to a class are correctly identified.

Recall = TP / (TP + FN)

### 9.4 F1-score

F1-score is the harmonic mean of precision and recall.

F1-score = 2 × (Precision × Recall) / (Precision + Recall)

### 9.5 Confusion Matrix

A confusion matrix compares actual class labels with predicted class labels.

It helps identify which disease categories are frequently confused with one another.

### 9.6 Generated Evaluation Reports

**RGB 3D-CNN reports**

- `reports/rgb_3dcnn_training_history.csv`
- `reports/rgb_3dcnn_classification_report.csv`
- `reports/rgb_3dcnn_confusion_matrix.png`
- `reports/rgb_3dcnn_metrics.json`
- `reports/rgb_3dcnn_independent_metrics.json`
- `reports/rgb_3dcnn_independent_classification_report.csv`
- `reports/rgb_3dcnn_independent_confusion_matrix.png`
- `reports/rgb_3dcnn_test_predictions.csv`

**DeiT-Tiny reports**

- `reports/deit_tiny_training_history.csv`
- `reports/deit_tiny_validation_report.csv`
- `reports/deit_tiny_validation_confusion_matrix.png`
- `reports/deit_tiny_validation_metrics.json`
- `reports/deit_tiny_test_metrics.json`
- `reports/deit_tiny_test_classification_report.csv`
- `reports/deit_tiny_test_confusion_matrix.png`
- `reports/deit_tiny_test_predictions.csv`

---

## 10. Limitations and Generalisation Risks

Although the models achieved promising results, several limitations must be considered.

### 10.1 RGB Dataset Limitation

The current dataset contains RGB images rather than hyperspectral images.

Therefore, the models cannot learn detailed wavelength-specific information that would be available from a true hyperspectral sensor.

### 10.2 Dataset Size

The final evaluation uses 336 test images.

A larger and more diverse dataset would provide stronger evidence of model generalisation.

### 10.3 Class Imbalance

The number of samples differs significantly across the four disease categories.

Black rot has only 11 test samples, which makes its evaluation metrics less stable.

### 10.4 Leaf Blight Classification

Leaf blight has comparatively weaker F1-scores across the evaluated architectures.

More representative training examples and further investigation may improve its recognition.

### 10.5 Environmental Variations

Images collected under different lighting conditions, camera types, backgrounds and geographical locations may affect prediction performance.

### 10.6 3D-CNN Interpretation

The experimental 3D-CNN uses RGB channels as its depth dimension.

It should not be considered a true spectral 3D-CNN because the dataset does not contain multiple wavelength bands.

### 10.7 Transformer Performance

DeiT-Tiny did not outperform the CNN-based models in this experiment.

Its performance may be affected by the dataset size, class distribution and the use of a frozen pretrained backbone.

### 10.8 Prediction Confidence

Softmax scores are not necessarily calibrated probabilities.

A high confidence score does not guarantee a correct disease prediction.

### 10.9 External Validation

The models have been evaluated using the available test split. Independent evaluation using images from different vineyards and collection environments is still required.

---

## 11. Reproducibility and Environment Setup

The project uses Python-based machine learning libraries and separate deep learning frameworks for the CNN and Vision Transformer experiments.

### 11.1 Tested Environment

| Component | Version / Configuration |
|---|---|
| Operating System | Windows |
| Python | 3.13.3 |
| TensorFlow | 2.21.0 |
| NumPy | 2.3.3 |
| Pandas | 2.3.3 |
| Scikit-learn | 1.7.2 |
| Matplotlib | 3.10.6 |
| PyTorch | 2.15.0+cpu |
| Transformers | 5.24.1 |
| Hardware | CPU |

The environment was tested without GPU acceleration.

### 11.2 Create a Virtual Environment

From the project root directory, execute:

`python -m venv .venv-ml`

Activate it using PowerShell:

`.venv-ml\Scripts\Activate.ps1`

### 11.3 Install CNN Dependencies

Install the direct dependencies listed in the project requirements file:

`pip install -r requirements-ml.txt`

The locked dependency file is also available:

`requirements-ml-lock.txt`

### 11.4 Vision Transformer Dependencies

The DeiT-Tiny experiment uses PyTorch and Hugging Face Transformers.

The tested environment used:

- PyTorch 2.15.0+cpu
- Transformers 5.24.1

The installed versions should be verified when recreating the environment.

### 11.5 Reproducibility Validation

The RGB 3D-CNN evaluation was successfully executed in a clean virtual environment using the documented TensorFlow-related dependencies.

The independent evaluation script reproduces the saved model's test metrics.

The DeiT-Tiny experiment was also trained and evaluated successfully in the tested CPU environment.

For complete independent reproduction of the DeiT experiment, its PyTorch, Transformers and image-processing dependencies must also be installed.

### 11.6 Main Scripts

| Script | Purpose |
|---|---|
| `src/train_3dcnn.py` | Train RGB 3D-CNN |
| `src/evaluate_3dcnn.py` | Independently evaluate RGB 3D-CNN |
| `src/inference_3dcnn.py` | Predict disease from a leaf image |
| `src/train_vit.py` | Train DeiT-Tiny |
| `src/evaluate_vit.py` | Evaluate DeiT-Tiny on the test split |

---

## 12. Model Files

### 12.1 Trained Model Checkpoints

| Model | Checkpoint |
|---|---|
| MobileNetV2 | `models/terraspectra_mobilenetv2_final.keras` |
| RGB 3D-CNN | `models/terraspectra_rgb_3dcnn_best.keras` |
| DeiT-Tiny | `models/terraspectra_deit_tiny_best/` |

The DeiT-Tiny checkpoint directory contains:

- `config.json`
- `model.safetensors`
- `preprocessor_config.json`

The model checkpoint files are maintained in the project repository branch used for this work.

---

## 13. Conclusion

TerraSpectra explores multiple deep learning architectures for RGB-based grapevine disease classification.

Three models were developed and evaluated:

1. MobileNetV2 as the baseline transfer learning model.
2. RGB 3D-CNN as an experimental 3D convolutional architecture.
3. DeiT-Tiny as a lightweight Vision Transformer comparison.

The RGB 3D-CNN achieved the highest test accuracy of 88.10% and macro F1-score of 0.7834 among the three evaluated models.

MobileNetV2 achieved 83.93% accuracy, while DeiT-Tiny achieved 81.25% accuracy on the same test split.

The project also includes preprocessing scripts, trained checkpoints, independent evaluation scripts, classification reports and confusion matrices.

The current results demonstrate the feasibility of applying different deep learning architectures to RGB grapevine disease classification.

### Future Work

Potential future improvements include:

- Collecting a larger and more balanced grapevine disease dataset.
- Evaluating the models on independent vineyard images.
- Improving Leaf blight and Black rot classification.
- Exploring model fine-tuning and hyperparameter optimization.
- Investigating hybrid CNN-Transformer architectures.
- Integrating actual hyperspectral data when a suitable dataset or sensor becomes available.
- Comparing RGB and hyperspectral approaches under a consistent experimental setup.

**Final Project Status:** The RGB-based MobileNetV2 baseline, experimental 3D-CNN and DeiT-Tiny comparison have been implemented and evaluated. True hyperspectral data processing and validation remain future work.
