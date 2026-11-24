# TerraSpectra – Data Science and Deep Learning Completion Report

**Date:** 24 November 2026  
**Contributor:** Nainesh  
**Branch:** nainesh  
**Target Branch:** main  
**Project:** TerraSpectra – Grapevine Disease Classification

## 1. Overview

The Data Science and Deep Learning development work for the TerraSpectra project has been completed and integrated into the main branch.

The primary objective was to develop a deep learning model capable of identifying grapevine leaf diseases from images and provide a reliable inference pipeline for backend integration.

## 2. Dataset Preparation

The following dataset preparation activities were completed:

- Analysed the GVLiD grapevine disease image dataset.
- Identified four classification categories:
  - Black rot
  - Esca
  - Healthy
  - Leaf blight
- Performed duplicate image detection and label conflict analysis.
- Identified duplicate leakage across the original dataset splits.
- Created a deduplicated final dataset split.
- Verified image paths and dataset integrity.

The final dataset split contains 2,407 unique images:

| Split | Images |
|---|---:|
| Training | 1,730 |
| Validation | 341 |
| Testing | 336 |
| **Total** | **2,407** |

## 3. Deep Learning Model Development

MobileNetV2 transfer learning was selected for the final model.

Development activities included:

- Implementing the MobileNetV2 architecture.
- Applying ImageNet pretrained weights.
- Performing transfer learning and fine-tuning.
- Applying class weighting to address class imbalance.
- Evaluating model performance using accuracy, precision, recall and F1-score.
- Analysing classification errors using a confusion matrix.

Final model:

`models/terraspectra_mobilenetv2_final.keras`

## 4. Final Model Performance

Evaluation results on the final test dataset:

| Metric | Result |
|---|---:|
| Test Accuracy | 83.93% |
| Macro F1-score | 0.7610 |
| Weighted F1-score | 0.8433 |

### Class-wise F1-score

| Disease Class | F1-score |
|---|---:|
| Black rot | 0.73 |
| Esca | 0.80 |
| Healthy | 0.99 |
| Leaf blight | 0.52 |

The results indicate strong performance for Healthy and Esca classification, while Leaf blight remains an area for improvement.

## 5. Inference Pipeline

A standalone inference module was implemented:

`src/inference.py`

The module provides the `GrapevineDiseasePredictor` class and handles:

- Loading the final trained model.
- Reading grapevine leaf images.
- Resizing images to 224 × 224 pixels.
- Applying MobileNetV2 preprocessing.
- Generating disease predictions.
- Returning confidence and class-wise prediction scores.

## 6. Inference Verification

Standalone inference was verified against notebook predictions.

| Verification | Result |
|---|---:|
| Notebook predictions | 336 |
| Standalone predictions | 336 |
| Matching predictions | 336 |
| Prediction parity | 100% |

This confirms consistency between the notebook and standalone inference implementation. It does not indicate 100% classification accuracy.

## 7. Backend Integration Handover

The inference module and final model are ready for backend integration.

The backend team can use `GrapevineDiseasePredictor` to generate predictions without implementing a separate image preprocessing pipeline.

The prediction response provides:

- Predicted disease
- Confidence score
- Class-wise prediction scores

## 8. GitHub Integration

The Data Science and Deep Learning contributions were developed in the `nainesh` branch and subsequently integrated into the `main` branch.

The integration includes:

- Dataset audit and final split preparation.
- Final MobileNetV2 model and training notebook.
- Model evaluation reports.
- Standalone inference implementation.
- Inference verification scripts.
- Model and inference handover documentation.

## 9. Future Improvements

Potential future improvements include:

- Increasing the number of Black rot and Leaf blight training samples.
- Improving classification performance for visually similar diseases.
- Evaluating additional augmentation techniques.
- Exploring model explainability using Grad-CAM.
- Monitoring inference performance after backend integration.

## 10. Conclusion

The Data Science and Deep Learning phase of TerraSpectra has reached its initial completion milestone.

The final MobileNetV2 model, evaluation reports, inference module and backend handover documentation have been integrated into the project's main branch.

The next phase can focus on backend integration, GIS dashboard connectivity and end-to-end application testing.