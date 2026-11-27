# TerraSpectra – RGB 3D-CNN Model Documentation

## 1. Project Overview

This document describes the dataset, preprocessing pipeline, RGB 3D-CNN architecture, model outputs, evaluation results and limitations of the TerraSpectra grapevine disease classification experiment.

**Important:** The current experiment uses RGB grapevine leaf images. It is not a hyperspectral imaging experiment. The three input channels represent Red, Green and Blue (RGB), not spectral wavelengths or hyperspectral bands.

## 2. Dataset Description

- Dataset: GVLiD grapevine leaf disease image dataset
- Total images: 3,477
- Image format: JPEG
- Original image dimensions: 1080 × 1080 pixels
- Image channels: 3 (RGB)
- Number of classes: 4

### Class labels

| Class ID | Disease class |
|---|---|
| 0 | Black rot |
| 1 | Esca |
| 2 | Healthy |
| 3 | Leaf blight |

### Dataset split

| Split | Number of images |
|---|---:|
| Training | 1,730 |
| Validation | 341 |
| Testing | 336 |
| **Total in final splits** | **2,407** |

The final split counts above describe the images used by the current model pipeline. They should not be confused with the total number of images in the original dataset.

## 3. Preprocessing Pipeline

The 3D-CNN preprocessing pipeline performs the following operations:

1. Reads the image using TensorFlow.
2. Decodes the JPEG image with three RGB channels.
3. Resizes the image to 64 × 64 pixels.
4. Converts pixel values to `float32`.
5. Normalizes pixel values by dividing by 255.
6. Rearranges the RGB channel dimension to the depth dimension.
7. Adds a final single-channel dimension.

### Preprocessing details

| Parameter | Value |
|---|---|
| Original image channels | 3 |
| Resized image dimensions | 64 × 64 |
| Data type | float32 |
| Normalization | Pixel value / 255 |
| Channel order | RGB (Red, Green, Blue) |
| Model input shape | (3, 64, 64, 1) |
| Batch size | 4 |
| Random seed | 42 |

### Tensor transformation

Original decoded image:

`(1080, 1080, 3)`

After resizing:

`(64, 64, 3)`

After rearranging RGB channels:

`(3, 64, 64)`

After adding the final dimension:

`(3, 64, 64, 1)`

**RGB channel/depth order:** Red → Green → Blue.

The depth dimension contains only the three RGB channels. It does not represent physical spectral bands or wavelength measurements.

## 4. RGB 3D-CNN Architecture

The model uses 3D convolution operations to process the transformed RGB input.

### Architecture summary

1. Input layer: `(3, 64, 64, 1)`
2. 3D convolution layer: 8 filters
3. 3D max-pooling layer
4. Batch normalization
5. 3D convolution layer: 16 filters
6. 3D max-pooling layer
7. Batch normalization
8. 3D convolution layer: 32 filters
9. Global average pooling
10. Dropout: 0.35
11. Dense output layer: 4 units with softmax activation

### Training configuration

| Parameter | Value |
|---|---|
| Optimizer | Adam |
| Learning rate | 0.001 |
| Loss function | Sparse categorical cross-entropy |
| Batch size | 4 |
| Maximum epochs | 15 |
| Random seed | 42 |
| Checkpoint selection | Best validation loss |
| Early stopping patience | 3 |

The best checkpoint is saved at:

`models/terraspectra_rgb_3dcnn_best.keras`

## 5. Model Output and Prediction Scores

The model predicts one of four classes:

- Black rot
- Esca
- Healthy
- Leaf blight

The final layer uses softmax activation and produces a score for each class.

The four output scores represent the model's estimated class probabilities. They sum approximately to 1.

The predicted class is the class with the highest output score.

**Confidence score:** The inference script displays the highest softmax score as the prediction confidence. This score is not a guarantee that the prediction is correct and should not be interpreted as a clinically or scientifically calibrated probability.

## 6. Evaluation Results

The model was evaluated on 336 test images.

### Overall performance

| Metric | Result |
|---|---:|
| Test accuracy | 88.10% |
| Macro precision | 0.8037 |
| Macro recall | 0.7890 |
| Macro F1-score | 0.7834 |
| Weighted F1-score | 0.8706 |
| Correct predictions | 296 / 336 |

### Per-class performance

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Black rot | 0.69 | 0.82 | 0.75 | 11 |
| Esca | 0.81 | 0.94 | 0.87 | 126 |
| Healthy | 1.00 | 0.99 | 1.00 | 150 |
| Leaf blight | 0.71 | 0.41 | 0.52 | 49 |

### Evaluation evidence

The project generates the following evaluation files:

- `reports/rgb_3dcnn_metrics.json`
- `reports/rgb_3dcnn_classification_report.csv`
- `reports/rgb_3dcnn_confusion_matrix.png`
- `reports/rgb_3dcnn_independent_metrics.json`
- `reports/rgb_3dcnn_independent_classification_report.csv`
- `reports/rgb_3dcnn_independent_confusion_matrix.png`
- `reports/rgb_3dcnn_test_predictions.csv`
- `reports/rgb_3dcnn_training_history.csv`

The independent evaluation script reproduces the test-set evaluation using the saved checkpoint and the same test split.

## 7. Limitations and Generalisation Risks

### 7.1 RGB instead of hyperspectral data

The current model uses ordinary RGB images. Its three-channel depth dimension does not contain hyperspectral wavelength information. Therefore, it cannot establish the benefits of hyperspectral imaging.

### 7.2 Class imbalance

The test set contains unequal numbers of images across the four classes. Healthy and Esca have substantially more test examples than Black rot.

### 7.3 Limited Black rot test samples

Only 11 Black rot images are present in the test set. Performance estimates for this class may therefore vary substantially with different test samples.

### 7.4 Low Leaf blight recall

Leaf blight recall is 0.41. This means the model misses a substantial proportion of actual Leaf blight cases in the test set. Further investigation and improvement are needed.

### 7.5 Generalisation to new environments

The current results do not establish performance on images from entirely new vineyards, cameras, lighting conditions, geographic regions or acquisition setups.

### 7.6 Prediction confidence

Softmax confidence should not be treated as certainty. The model may produce high confidence for an incorrect prediction.

### 7.7 Test-set limitations

The reported test metrics describe performance on the current held-out test split. Repeatedly using the test set to tune model decisions can lead to optimistic estimates. Further validation on an independent dataset is recommended.

## 8. Reproducibility

The project includes separate scripts for training, evaluation and inference:

- `src/train_3dcnn.py`
- `src/evaluate_3dcnn.py`
- `src/inference_3dcnn.py`

The scripts have been executed successfully in the current Windows environment with TensorFlow 2.21.0.

However, execution in a completely clean environment has not yet been verified. Dependency documentation and a fresh-environment test remain outstanding.

## 9. Model Files and Usage

### Model checkpoint

`models/terraspectra_rgb_3dcnn_best.keras`

### Training

```bash
python src/train_3dcnn.py
```

### Evaluation

```bash
python src/evaluate_3dcnn.py
```

### Single-image inference

```bash
python src/inference_3dcnn.py "path/to/leaf_image.jpg"
```

## 10. Conclusion

The RGB 3D-CNN achieved 88.10% accuracy and a macro F1-score of 0.7834 on the current test split. It performs well on Healthy and Esca images, while Leaf blight recall remains an important area for improvement.

This experiment demonstrates an RGB-based 3D-CNN classification approach. It should not be presented as a hyperspectral model. Further work should focus on reproducibility, validation on independent data, class-wise performance improvements and comparison with alternative architectures such as Vision Transformers or hybrid models.



## Clean Environment Reproducibility Validation

A fresh Python virtual environment was created and tested successfully on Windows.

**Environment**
- Python: 3.13.3
- TensorFlow: 2.21.0
- NumPy: 2.3.3
- Pandas: 2.3.3
- Scikit-learn: 1.7.2
- Matplotlib: 3.10.6

**Validation procedure**
1. Created a fresh environment using `python -m venv .venv-ml`.
2. Installed dependencies using `pip install -r requirements-ml.txt`.
3. Loaded the saved RGB 3D-CNN checkpoint.
4. Evaluated the model on all 336 test images.
5. Reproduced the previously reported evaluation metrics.

**Verified results**
- Accuracy: 88.10%
- Macro Precision: 0.8037
- Macro Recall: 0.7890
- Macro F1-score: 0.7834
- Weighted F1-score: 0.8706

The clean-environment evaluation completed successfully.

The test was performed using native Windows CPU TensorFlow. GPU acceleration was unavailable in this environment.
