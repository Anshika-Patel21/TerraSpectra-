# TerraSpectra – Model and Inference Handover

**Last updated:** 23 November 2026  
**Owner:** Data Science and Deep Learning  
**Final Model:** MobileNetV2 Transfer Learning (v4)

## 1. Final Model

The selected model is:

`models/terraspectra_mobilenetv2_final.keras`

It classifies grapevine leaf images into four categories:

1. Black rot
2. Esca
3. Healthy
4. Leaf blight

## 2. Input Requirements

- Image size: 224 × 224 pixels
- Colour channels: RGB
- Input preprocessing: MobileNetV2 `preprocess_input`
- Preprocessed pixel range: approximately [-1, 1]

The inference module handles image decoding, resizing and preprocessing.

## 3. Model Evaluation

Evaluation was performed on the final test split containing 336 images.

| Metric | Result |
|---|---:|
| Accuracy | 83.93% |
| Macro F1-score | 0.7610 |
| Weighted F1-score | 0.8433 |

### Class-wise Performance

| Class | F1-score | Test Images |
|---|---:|---:|
| Black rot | 0.73 | 11 |
| Esca | 0.80 | 126 |
| Healthy | 0.99 | 150 |
| Leaf blight | 0.52 | 49 |

Black rot has limited test representation, while Leaf blight remains a challenging classification category.

## 4. Inference Module

Backend integration should use:

`src/inference.py`

The module provides the `GrapevineDiseasePredictor` class.

### Example Usage

```python
from src.inference import GrapevineDiseasePredictor

predictor = GrapevineDiseasePredictor()

result = predictor.predict("path/to/grapevine_leaf.jpg")

print(result)
```

### Prediction Response

The response contains:

- `predicted_disease`: Predicted disease class.
- `confidence`: Confidence score between 0 and 1.
- `probabilities`: Scores for all four classes.

The backend should use this existing inference module rather than implementing a separate preprocessing pipeline.

## 5. Standalone Inference Verification

Run the following command from the project root:

```powershell
python src/verify_inference.py
```

The script evaluates all 336 test images and saves predictions to:

`reports/standalone_test_predictions.csv`

### Verification Result

- Notebook predictions: 336
- Standalone predictions: 336
- Matching predictions: 336
- Prediction parity: 100%

This confirms that standalone inference produces the same predictions as the evaluated notebook. It does not mean the model has 100% accuracy.

## 6. Important Project Files

| File | Purpose |
|---|---|
| `models/terraspectra_mobilenetv2_final.keras` | Final trained model |
| `src/inference.py` | Backend prediction interface |
| `src/verify_inference.py` | Standalone inference verification |
| `notebooks/08_mobilenetv2_transfer_learning_v4.ipynb` | Final model training and evaluation |
| `reports/final_classification_report.csv` | Class-wise evaluation results |
| `reports/model_metrics.json` | Model evaluation metrics |
| `reports/terraspectra_final_confusion_matrix.png` | Confusion matrix |
| `reports/inference_parity_comparison.csv` | Notebook and standalone prediction comparison |

## 7. Dataset and Evaluation Limitations

- Duplicate images were audited before creating the final dataset split.
- Two exact duplicate groups with conflicting labels were excluded.
- The final split uses unique-image representatives and representative-vineyard grouping.
- Original duplicate-to-vineyard associations mean this should not be described as a fully independent vineyard-level split.
- Black rot has limited representation in the final test set.
- Leaf blight remains a challenging class and may be confused with Esca.

These limitations should be considered when interpreting model performance.

## 8. Backend Handover Notes

1. Load the final `.keras` model using `GrapevineDiseasePredictor`.
2. Use the existing `predict()` method for image predictions.
3. Maintain the same 224 × 224 RGB input and MobileNetV2 preprocessing.
4. Return the predicted disease, confidence score and class-wise scores through the backend API.
5. Treat confidence as a model score, not a guarantee of prediction correctness.

**Status:** Model training, final evaluation, standalone inference verification and backend inference handover are completed.