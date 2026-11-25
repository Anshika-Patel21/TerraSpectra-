# TerraSpectra – Dataset Quality Audit and Split Documentation

**Date:** 25 November 2026  
**Contributor:** Data Science and Deep Learning Team

## 1. Dataset Overview

The project uses the GVLiD grapevine leaf disease image dataset for four-class disease classification.

The four categories are:
- Black rot
- Esca
- Healthy
- Leaf blight

The original dataset contains 3,477 image files.

## 2. Duplicate Image Audit

A duplicate image audit was performed using image hashes.

| Audit Metric | Result |
|---|---:|
| Total image files checked | 3,477 |
| Unique image hashes | 2,409 |
| Duplicate groups | 446 |
| Files involved in duplicate groups | 1,514 |
| Duplicate groups crossing original splits | 246 |
| Conflicting-label duplicate groups | 2 |

The audit identified duplicate leakage across the original dataset splits. Two exact duplicate groups with conflicting labels were excluded from the final unique dataset.

## 3. Final Dataset Preparation

The final dataset was prepared using unique image representatives and representative-vineyard grouping.

| Dataset Split | Image Count |
|---|---:|
| Training | 1,730 |
| Validation | 341 |
| Testing | 336 |
| **Total** | **2,407** |

All image paths in the final split were verified.

## 4. Important Evaluation Considerations

- Duplicate leakage was addressed before final model evaluation.
- The final split avoids overlap in representative image hashes.
- Representative-vineyard grouping does not eliminate every original vineyard association because duplicate images can be associated with multiple vineyards.
- Therefore, the split should not be described as a fully independent vineyard-level split.
- Black rot has limited representation in the test set.

## 5. Conclusion

The dataset audit improved the reliability of model evaluation by identifying duplicate images and label conflicts before final training and testing.

These dataset limitations should be considered when interpreting the TerraSpectra MobileNetV2 model's performance.