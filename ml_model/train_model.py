"""
ML Model Training Script for Placement Prediction

This script trains a Random Forest classifier to predict student placement
based on CGPA, internships, projects, and communication skills.

Usage:
    python ml_model/train_model.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

def generate_sample_data(n_samples=200):
    """
    Generate synthetic training data for placement prediction
    
    In production, replace this with actual historical placement data
    """
    np.random.seed(42)
    
    data = {
        'cgpa': np.random.uniform(5.0, 10.0, n_samples),
        'internships': np.random.randint(0, 5, n_samples),
        'projects': np.random.randint(0, 8, n_samples),
        'communication': np.random.randint(1, 11, n_samples),
    }
    
    # Create placement outcome based on weighted features
    # Higher CGPA, more internships/projects, better communication = higher placement chance
    placement_score = (
        data['cgpa'] * 0.4 +
        data['internships'] * 1.5 +
        data['projects'] * 1.0 +
        data['communication'] * 0.5 +
        np.random.normal(0, 2, n_samples)  # Add some randomness
    )
    
    # Convert to binary outcome (threshold-based)
    threshold = np.percentile(placement_score, 40)  # 60% placement rate
    data['placement'] = (placement_score > threshold).astype(int)
    
    return pd.DataFrame(data)


def train_model():
    """Train and evaluate the placement prediction model"""
    
    print("=" * 60)
    print("PLACEMENT PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    # Generate or load data
    print("\n📊 Loading training data...")
    df = generate_sample_data(n_samples=200)
    
    print(f"Dataset size: {len(df)} samples")
    print(f"Placement rate: {df['placement'].mean():.2%}")
    print("\nFeature statistics:")
    print(df.describe())
    
    # Features and label
    X = df[['cgpa', 'internships', 'projects', 'communication']]
    y = df['placement']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📈 Training set: {len(X_train)} samples")
    print(f"📉 Test set: {len(X_test)} samples")
    
    # Train model
    print("\n🤖 Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate model
    print("\n✅ Model training complete!")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"\n📊 Cross-validation scores: {cv_scores}")
    print(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Test set evaluation
    y_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n🎯 Test set accuracy: {test_accuracy:.4f}")
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Placed', 'Placed']))
    
    print("\n🔢 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n⭐ Feature Importance:")
    print(feature_importance.to_string(index=False))
    
    # Save model
    model_dir = os.path.dirname(__file__)
    model_path = os.path.join(model_dir, 'placement_model.pkl')
    
    joblib.dump(model, model_path)
    print(f"\n💾 Model saved to: {model_path}")
    
    # Save to ml_models directory as well
    alt_model_dir = os.path.join(os.path.dirname(model_dir), 'ml_models')
    if os.path.exists(alt_model_dir):
        alt_model_path = os.path.join(alt_model_dir, 'placement_class_model.joblib')
        joblib.dump(model, alt_model_path)
        print(f"💾 Model also saved to: {alt_model_path}")
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    
    return model


if __name__ == "__main__":
    train_model()
