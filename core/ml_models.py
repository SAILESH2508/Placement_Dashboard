# core/ml_models.py
import os
import joblib
import numpy as np
import pandas as pd
from django.conf import settings
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, roc_auc_score, mean_absolute_error, r2_score

MODEL_DIR = os.path.join(settings.BASE_DIR, 'ml_models')
os.makedirs(MODEL_DIR, exist_ok=True)

# simple branch mapping if you prefer label encoding — we'll use one-hot in pipeline
CATEGORICAL_FEATURES = ['branch']
NUMERIC_FEATURES = ['cgpa', 'year']

CLASS_MODEL_PATH = os.path.join(MODEL_DIR, 'placement_class_model.joblib')
REG_MODEL_PATH = os.path.join(MODEL_DIR, 'package_reg_model.joblib')
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, 'preprocessor.joblib')

def build_preprocessor():
    # One-hot encode branch, passthrough numeric
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', ohe, CATEGORICAL_FEATURES),
            ('num', 'passthrough', NUMERIC_FEATURES),
        ],
        remainder='drop'
    )
    return preprocessor

def train_models(df, target_col='placed', package_col='package_lpa', random_state=42):
    """
    df: pandas DataFrame with columns: branch, cgpa, year, placed (0/1), package_lpa
    returns: dict with metrics
    """
    # Ensure required columns
    for col in CATEGORICAL_FEATURES + NUMERIC_FEATURES + [target_col, package_col]:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    X = df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y_class = df[target_col].astype(int)
    y_reg = df[package_col].fillna(0.0).astype(float)

    preprocessor = build_preprocessor()
    X_trans = preprocessor.fit_transform(X)
    # Save preprocessor
    joblib.dump(preprocessor, PREPROCESSOR_PATH)

    # Classification model: LogisticRegression
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_trans, y_class, test_size=0.2, random_state=random_state)
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_c, y_train_c)
    preds_c = clf.predict(X_test_c)
    probs_c = clf.predict_proba(X_test_c)[:, 1]
    acc = accuracy_score(y_test_c, preds_c)
    auc = roc_auc_score(y_test_c, probs_c)

    joblib.dump(clf, CLASS_MODEL_PATH)

    # Regression model: RandomForestRegressor
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_trans, y_reg, test_size=0.2, random_state=random_state)
    reg = RandomForestRegressor(n_estimators=100, random_state=random_state)
    reg.fit(X_train_r, y_train_r)
    preds_r = reg.predict(X_test_r)
    mae = mean_absolute_error(y_test_r, preds_r)
    r2 = r2_score(y_test_r, preds_r)

    joblib.dump(reg, REG_MODEL_PATH)

    return {
        'classification': {'accuracy': float(acc), 'auc': float(auc)},
        'regression': {'mae': float(mae), 'r2': float(r2)},
        'paths': {
            'preprocessor': PREPROCESSOR_PATH,
            'classifier': CLASS_MODEL_PATH,
            'regressor': REG_MODEL_PATH
        }
    }

def load_models():
    """Load preprocessor, classifier, regressor. Raises if missing."""
    if not (os.path.exists(PREPROCESSOR_PATH) and os.path.exists(CLASS_MODEL_PATH) and os.path.exists(REG_MODEL_PATH)):
        raise FileNotFoundError("One or more ML model files are missing. Train the models first with management command.")
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    clf = joblib.load(CLASS_MODEL_PATH)
    reg = joblib.load(REG_MODEL_PATH)
    return preprocessor, clf, reg

def predict_single(sample: dict):
    """
    sample: dict with keys: branch, cgpa, year
    returns: dict with probability and package prediction
    """
    preprocessor, clf, reg = load_models()
    X_df = pd.DataFrame([sample])
    X_trans = preprocessor.transform(X_df)
    prob = float(clf.predict_proba(X_trans)[:, 1][0])
    package_pred = float(reg.predict(X_trans)[0])
    return {'placement_probability': prob, 'predicted_package_lpa': package_pred}
