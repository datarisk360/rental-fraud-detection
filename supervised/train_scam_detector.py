
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load dataset
df = pd.read_csv('train.csv')

# Select features and target
features = [
    'LISTING_KIND', 'LISTING_CITY', 'LISTING_PRICE',
    'IS_ARCHIVED', 'LOGIN_COUNTRY_CODE', 'LISTING_COUNTRY_CODE',
    'LISTING_REGISTRATION_POSSIBLE', 'ADVERTISER_COMPLETENESS_SCORE',
    'MANAGED_ACCOUNT', 'HAS_PROFILE_PIC', 'BROWSER', 'OS'
]
target = 'IS_SCAMMER'

# Filter relevant columns
X = df[features]
y = df[target]

# One-hot encode categorical variables
X_encoded = pd.get_dummies(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model
joblib.dump(model, 'scam_detector_model.joblib')
print("✅ Model saved as 'scam_detector_model.joblib'")
