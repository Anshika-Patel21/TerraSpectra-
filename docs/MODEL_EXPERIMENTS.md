# TerraSpectra – Model Experiments

## Experiment 1: Baseline CNN v1

**Architecture:** 3 convolutional layers, Flatten, Dense, Dropout, Softmax.

- Total parameters: 11,169,476
- Training: 20 epochs
- Initial validation performance was poor.
- The model did not demonstrate satisfactory generalization.

### Observation
The large Flatten and Dense layers resulted in a high parameter count. This architecture was not selected as the primary model.

---

## Experiment 2: Improved CNN v2

### Architecture
- 4 convolutional blocks
- Batch Normalization
- Max Pooling
- Global Average Pooling
- Dense layer with 128 units
- Dropout (0.4)
- Softmax output with 4 classes

### Model Configuration
- Optimizer: Adam
- Initial learning rate: 0.0001
- Loss function: Sparse Categorical Crossentropy
- Batch size: 32
- Maximum epochs: 20
- Early Stopping
- Model Checkpoint
- ReduceLROnPlateau

### Model Size
- Total parameters: 423,748
- Trainable parameters: 422,788
- Non-trainable parameters: 960
- Approximate size: 1.62 MB

### Test Results

| Metric | Value |
|---|---:|
| Test Accuracy | 88.53% |
| Test Loss | 0.2328 |
| Weighted Precision | 88.31% |
| Weighted Recall | 88.53% |
| Weighted F1-score | 88.40% |
| Macro F1-score | 86.71% |

### Class-wise Performance

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Black rot | 97.14% | 99.03% | 98.08% |
| Esca | 80.15% | 81.40% | 80.77% |
| Healthy | 99.32% | 100.00% | 99.66% |
| Leaf blight | 70.51% | 66.27% | 68.32% |

### Confusion Matrix Analysis

The model achieved excellent performance for Healthy and Black rot images.

The primary classification challenge is distinguishing Esca from Leaf Blight:

- 23 Esca images were classified as Leaf Blight.
- 25 Leaf Blight images were classified as Esca.
- 3 Leaf Blight images were classified as Black rot.
- 1 Black rot image was classified as Esca.

### Conclusion

CNN v2 significantly improved the baseline architecture and achieved 88.53% test accuracy with a relatively lightweight model.

The next experiment will investigate transfer learning using MobileNetV2 to improve disease classification, particularly for Esca and Leaf Blight.


## Experiment 2: MobileNetV2 Transfer Learning

**Date:** 18 November 2026  
**Dataset:** GVLiD  
**Input Size:** 224 × 224 RGB  
**Classes:** Black rot, Esca, Healthy, Leaf blight

### Architecture

MobileNetV2 pretrained on ImageNet was used as the feature extraction backbone.

**Phase 1 – Feature Extraction**
- Base model: MobileNetV2
- Pretrained weights: ImageNet
- Backbone frozen
- Global Average Pooling
- Dropout: 0.3
- Dense output layer: 4 classes
- Optimizer: Adam
- Learning rate: 0.001
- Training epochs: 10

**Phase 2 – Fine-tuning**
- Unfrozen final layers of MobileNetV2
- Batch Normalization layers frozen
- Trainable parameters: 1,515,844
- Optimizer: Adam
- Learning rate: 0.00001
- Fine-tuning epochs: 5
- Best checkpoint: Epoch 4

### Performance

| Metric | Result |
|---|---:|
| Validation Accuracy | 87.55% |
| Test Accuracy | 85.50% |
| Test Loss | 0.3019 |
| Macro F1-score | 0.8328 |
| Weighted F1-score | 0.8535 |

### Class-wise Performance

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Black rot | 97.17% | 100.00% | 98.56% |
| Esca | 74.44% | 76.74% | 75.57% |
| Healthy | 99.32% | 98.64% | 98.98% |
| Leaf blight | 62.34% | 57.83% | 60.00% |

### Key Findings

- MobileNetV2 achieved strong classification performance for Healthy and Black rot.
- Esca and Leaf blight remain the most challenging disease classes.
- The confusion matrix shows significant misclassification between Esca and Leaf blight.
- Fine-tuning improved validation accuracy from 86.33% to 87.55%.
- The final test accuracy was 85.50%.

### Model Comparison

Custom CNN v2 achieved 88.53% test accuracy, outperforming fine-tuned MobileNetV2 at 85.50%.

Custom CNN v2 is currently selected as the best-performing model based on test accuracy, test loss, and macro F1-score. MobileNetV2 is retained as a transfer-learning comparison experiment.



## Day 6 – Error Analysis and Data Augmentation

### 1. Baseline CNN v2 Error Analysis

The baseline CNN v2 achieved 88.16% validation accuracy.

The major classification errors were observed between Esca and
Leaf Blight. This indicates visual similarity between these disease
categories may be affecting model predictions.

### 2. Strong Data Augmentation Experiment

Applied:
- Random horizontal and vertical flipping
- Random rotation (0.08)
- Random zoom (0.10)
- Random contrast (0.10)

Results:
- Validation Accuracy: 83.88%
- Macro F1: 0.8258
- Weighted F1: 0.8393

Strong augmentation did not improve overall model performance.

### 3. Moderate Data Augmentation Experiment

Applied:
- Random horizontal flipping
- Random rotation (0.03)
- Random zoom (0.05)
- Random contrast (0.05)

Results:
- Validation Accuracy: 86.33%
- Macro F1: 0.8489
- Weighted F1: 0.8620

Moderate augmentation improved Esca recall but reduced overall
accuracy compared with the baseline.

### 4. Model Comparison

| Model | Validation Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| Baseline CNN v2 | 88.16% | ~0.8700 | ~0.8800 |
| Strong Augmentation CNN | 83.88% | 0.8258 | 0.8393 |
| Moderate Augmentation CNN | 86.33% | 0.8489 | 0.8620 |

### 5. Model Selection

Baseline CNN v2 was selected as the leading model because it
achieved the highest validation accuracy and macro F1 among the
three experiments.

The test dataset will remain reserved for final evaluation.


## Day 6 – Final Test Evaluation

### Selected Model: Baseline CNN v2

After comparing the baseline CNN, strong augmentation CNN, and moderate augmentation CNN, Baseline CNN v2 was selected based on its superior validation performance.

### Final Test Results

- Test samples: 462
- Test accuracy: 87.01%
- Test loss: 0.2548
- Macro F1-score: 0.8486
- Weighted F1-score: 0.8687

### Class-wise Performance

| Disease | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Black rot | 0.9623 | 0.9903 | 0.9761 |
| Esca | 0.7786 | 0.7907 | 0.7846 |
| Healthy | 1.0000 | 1.0000 | 1.0000 |
| Leaf blight | 0.6538 | 0.6145 | 0.6335 |

### Confusion Matrix Observations

- Healthy images achieved 100% classification accuracy.
- Black rot achieved 99.03% recall.
- Esca and Leaf blight showed considerable classification confusion.
- 27 Esca images were classified as Leaf blight.
- 28 Leaf blight images were classified as Esca.

### Final Conclusion

Baseline CNN v2 achieved 87.01% accuracy on the reserved test dataset.

The model demonstrated strong performance in identifying Healthy and Black rot grapevine leaves. However, distinguishing Esca and Leaf blight remains a challenge.

The baseline CNN v2 is retained as the selected model for the current project stage.