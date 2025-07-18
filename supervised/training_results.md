# Model Training Results – Supervised Scam Detector

**Model:** RandomForestClassifier  
**Parameters:** 100 estimators, random_state=42  
**Features used:** 12  
**Target variable:** `IS_SCAMMER` (0 = not scam, 1 = scam)

---

## Dataset Overview

| Description                 | Count         |
|-----------------------------|---------------|
| Original dataset size       | ~16,800 rows  |
| Subset for testing accuracy | 3,352 rows    |
| Labeled fraud cases in test| 199 scams     |

---

## Automatic Validation (`train_test_split`)

Performed on an 80/20 split from the labeled dataset (2,682 rows used):

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0 (not scam) | 0.99 | 0.99 | 0.99 | 2534 |
| 1 (scam)     | 0.88 | 0.79 | 0.83 | 148 |

- **Accuracy:** ~98%  
- **Macro avg F1:** 0.91  
- **Weighted avg F1:** 0.98

### Confusion Matrix:

|              | Predicted: 0 | Predicted: 1 |
|--------------|--------------|--------------|
| **Actual: 0** |     2,518    |      16      |
| **Actual: 1** |      31      |     117      |

---

## Manual Validation – Real-World Subset (3,352 rows)

To assess real-world generalization, the model was tested on a manually curated set of 3,352 listings containing 199 known scam cases.

| Metric             | Value        |
|--------------------|--------------|
| Expected frauds    | 199          |
| Detected frauds    | 176          |
| True positives     | 161          |
| False positives    | 15           |
| **Recall**         | 81%          |
| **Precision**      | 91%          |
| **Accuracy**       | ~98.4%       |

### Confusion Matrix (manual test):

|              | Predicted: 0 | Predicted: 1 |
|--------------|--------------|--------------|
| **Actual: 0** |     3,138    |      15      |
| **Actual: 1** |      38      |     161      |

> Compared to the internal test split (recall = 79%, precision = 88%, accuracy ≈ 98%), the model slightly improved in real-world validation, showing robust generalization.

---

## Conclusion

The model is stable and performs consistently across both internal and external evaluations, maintaining high precision and low false positive rates — crucial in fraud detection.

The trained model is saved as: `scam_detector_model.joblib`
