# TerraSpectra – Final ML Handoff and Evidence Summary

**Date:** 28 November 2026  
**Contributor:** Nainesh  
**Working Branch:** `nainesh`

## 1. Purpose

This document provides a consolidated summary of the machine learning implementation, evaluation results, reproducibility evidence and handoff status for the TerraSpectra grapevine disease classification project.

It complements `ML_DELIVERABLES.md`, which contains the detailed technical documentation.

## 2. Completed ML Deliverables

| Deliverable | Status | Evidence |
|---|---|---|
| Reproducible preprocessing | Completed and tested | Training and evaluation scripts |
| RGB 3D-CNN training | Completed | Training script and checkpoint |
| 3D-CNN evaluation | Completed | Metrics, classification report and confusion matrix |
| DeiT-Tiny comparison | Completed | Training and evaluation scripts and reports |
| MobileNetV2 baseline preservation | Completed | Existing baseline checkpoint and metrics |
| Per-class evaluation | Completed | Classification reports |
| Inference implementation | Completed | Model-specific inference scripts |
| Technical documentation | Completed | `docs/ML_DELIVERABLES.md` |
| Dependency documentation | Completed | `requirements-ml.txt`, `requirements-vit.txt` |

## 3. Model Comparison

All three models were evaluated on the same test set of 336 images.

| Model | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| MobileNetV2 | 83.93% | 0.7610 | 0.8433 |
| RGB 3D-CNN | 88.10% | 0.7834 | 0.8706 |
| DeiT-Tiny | 81.25% | 0.6970 | 0.8146 |

The RGB 3D-CNN achieved the highest test accuracy and macro F1 among the three evaluated models.

These results are preliminary and should be interpreted with the dataset size, class imbalance and per-class performance in mind.

## 4. Model and Evidence Locations

### RGB 3D-CNN

- Checkpoint: `models/terraspectra_rgb_3dcnn_best.keras`
- Training script: `src/train_3dcnn.py`
- Evaluation script: `src/evaluate_3dcnn.py`
- Inference script: `src/inference_3dcnn.py`
- Metrics: `reports/rgb_3dcnn_metrics.json`
- Classification report: `reports/rgb_3dcnn_classification_report.csv`
- Confusion matrix: `reports/rgb_3dcnn_confusion_matrix.png`

### DeiT-Tiny

- Checkpoint directory: `models/terraspectra_deit_tiny_best/`
- Training script: `src/train_vit.py`
- Evaluation script: `src/evaluate_vit.py`
- Metrics: `reports/deit_tiny_test_metrics.json`
- Classification report: `reports/deit_tiny_test_classification_report.csv`
- Confusion matrix: `reports/deit_tiny_test_confusion_matrix.png`

### MobileNetV2 Baseline

- Checkpoint: `models/terraspectra_mobilenetv2_final.keras`

### Environment and Dependencies

- TensorFlow dependencies: `requirements-ml.txt`
- DeiT-Tiny dependencies: `requirements-vit.txt`
- Locked environment: `requirements-ml-lock.txt`

## 5. Dataset and Input Clarification

The current experiments use the RGB grapevine leaf image dataset.

The dataset contains four disease categories:

1. Black rot
2. Esca
3. Healthy
4. Leaf blight

The RGB 3D-CNN transforms the three RGB channels into a depth dimension, producing an input tensor of shape `(3, 64, 64, 1)`.

**Important:** These three depth positions represent RGB channels, not actual hyperspectral bands or wavelengths. The current results must therefore be described as RGB image-based experiments, not hyperspectral disease classification.

## 6. Evaluation and Limitations

The test set contains 336 images. Class-wise support is limited for some categories, particularly Black rot.

The RGB 3D-CNN achieved an overall accuracy of 88.10%, but Leaf blight recall was only 0.41. This indicates that further improvement is needed for that category.

Other limitations include:

- Class imbalance in the dataset.
- Limited test samples for certain disease classes.
- Potential differences in lighting, image quality, vineyard conditions and camera devices.
- No guarantee of generalisation to unseen vineyards or field conditions.
- Prediction probabilities should not be interpreted as guaranteed diagnostic certainty.

## 7. Handoff Verification

The following items should be verified during final team handoff:

- [x] Training and evaluation scripts committed to the working branch.
- [x] Model checkpoints committed to the working branch.
- [x] Evaluation reports and confusion matrices generated.
- [x] Dataset, preprocessing and model limitations documented.
- [x] Dependency files committed.
- [ ] Alphia confirms successful access to and loading of the final 3D-CNN checkpoint.
- [ ] Team confirms the RGB dataset scope is understood.

## 8. Repository Status

The ML implementation and documentation updates are maintained on the `nainesh` branch.

The latest documented commit before this handoff update is:

`1b2a5ec` – Document DeiT dependencies and complete ML deliverables.

The `main` branch is intentionally unchanged at this stage.

## 9. Conclusion

The core ML implementation, model comparison, evaluation, inference and documentation work has been completed and pushed to the `nainesh` branch.

The remaining handoff activities concern team-side checkpoint access verification and confirmation of the dataset scope.