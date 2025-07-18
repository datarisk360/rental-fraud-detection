# Supervised Scam Detection Model

This folder contains a supervised machine learning model for identifying potentially fraudulent rental listings.

---

## Model Overview

- **Type:** Random Forest Classifier
- **Trained on:** Labeled dataset with known scam/non-scam listings
- **Features used:** 12 metadata fields per listing
- **Output:** Binary prediction – scam (1) or not scam (0)

---

## Files

| File                        | Description |
|-----------------------------|-------------|
| `train_scam_detector.py`    | Trains the model on labeled data and saves a `.joblib` file |
| `predict_scam.py`           | Loads the model and applies it to new listings |
| `scam_detector_model.joblib`| The trained classifier, serialized with `joblib` |
| `training_results.md`       | Evaluation metrics, confusion matrix, and manual validation results |

---

## Performance

- **Internal test split:** ~98% accuracy, 0.83 F1-score on scams  
- **Manual validation (real-world subset, 3,352 rows):**  
  - **Accuracy:** ~98.4%  
  - **Recall:** 81%  
  - **Precision:** 91%

See [`training_results.md`](training_results.md) for full details.

---

## Features Used

- `LISTING_KIND`
- `LISTING_CITY`
- `LISTING_PRICE`
- `IS_ARCHIVED`
- `LOGIN_COUNTRY_CODE`
- `LISTING_COUNTRY_CODE`
- `LISTING_REGISTRATION_POSSIBLE`
- `ADVERTISER_COMPLETENESS_SCORE`
- `MANAGED_ACCOUNT`
- `HAS_PROFILE_PIC`
- `BROWSER`
- `OS`

All categorical features are one-hot encoded.

---

## How to Use

Install dependencies:

```bash
pip install pandas scikit-learn joblib
