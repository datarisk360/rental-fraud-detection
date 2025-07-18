import pandas as pd
import joblib

# Load trained model
model = joblib.load('scam_detector_model.joblib')

# Load new data (same structure but with IS_SCAMMER empty or missing)
df = pd.read_csv('check.csv')

# Features used for prediction
features = [
    'LISTING_KIND', 'LISTING_CITY', 'LISTING_PRICE',
    'IS_ARCHIVED', 'LOGIN_COUNTRY_CODE', 'LISTING_COUNTRY_CODE',
    'LISTING_REGISTRATION_POSSIBLE', 'ADVERTISER_COMPLETENESS_SCORE',
    'MANAGED_ACCOUNT', 'HAS_PROFILE_PIC', 'BROWSER', 'OS'
]

# Keep original data for merging
df_original = df.copy()

# Prepare input data
X = df[features]
X_encoded = pd.get_dummies(X)

# Ensure same columns as training (add missing if any)
model_features = model.feature_names_in_
for col in model_features:
    if col not in X_encoded.columns:
        X_encoded[col] = 0
X_encoded = X_encoded[model_features]

# Make predictions
predictions = model.predict(X_encoded)

# Add predictions to original dataframe
df_original['IS_SCAMMER_PREDICTED'] = predictions

# Save output
df_original.to_csv('check_with_predictions.csv', index=False)
print("✅ Predictions saved in 'check_with_predictions.csv'")

