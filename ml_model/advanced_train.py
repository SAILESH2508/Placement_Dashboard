"""
Advanced ML Model Training with Multiple Algorithms
Trains and compares different models for placement prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

def generate_enhanced_data(n_samples=500):
    """Generate more realistic training data with additional features"""
    np.random.seed(42)
    
    data = {
        'cgpa': np.random.uniform(5.0, 10.0, n_samples),
        'internships': np.random.randint(0, 6, n_samples),
        'projects': np.random.randint(0, 10, n_samples),
        'communication': np.random.randint(1, 11, n_samples),
        'coding_score': np.random.randint(0, 101, n_samples),  # New feature
        'aptitude_score': np.random.randint(0, 101, n_samples),  # New feature
    }
    
    # Create placement outcome with more realistic logic
    placement_score = (
        data['cgpa'] * 0.25 +
        data['internships'] * 1.2 +
        data['projects'] * 0.8 +
        data['communication'] * 0.4 +
        data['coding_score'] * 0.05 +
        data['aptitude_score'] * 0.03 +
        np.random.normal(0, 2, n_samples)
    )
    
    # Convert to binary with threshold
    threshold = np.percentile(placement_score, 35)  # 65% placement rate
    data['placement'] = (placement_score > threshold).astype(int)
    
    return pd.DataFrame(data)


def plot_feature_importance(model, feature_names, save_path):
    """Plot and save feature importance"""
    if hasattr(model, 'feature_importances_'):
        importance = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=importance, x='importance', y='feature', palette='viridis')
        plt.title('Feature Importance', fontsize=16, fontweight='bold')
        plt.xlabel('Importance Score')
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        
        return importance
    return None


def plot_confusion_matrix(y_true, y_pred, save_path):
    """Plot and save confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_roc_curve(y_true, y_pred_proba, save_path):
    """Plot and save ROC curve"""
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    auc_score = roc_auc_score(y_true, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, linewidth=2, label=f'ROC Curve (AUC = {auc_score:.3f})')
    plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def train_and_compare_models():
    """Train multiple models and compare performance"""
    
    print("=" * 70)
    print("ADVANCED PLACEMENT PREDICTION MODEL TRAINING")
    print("=" * 70)
    
    # Generate data
    print("\n📊 Generating enhanced training data...")
    df = generate_enhanced_data(n_samples=500)
    
    print(f"Dataset size: {len(df)} samples")
    print(f"Placement rate: {df['placement'].mean():.2%}")
    print("\nFeature statistics:")
    print(df.describe())
    
    # Prepare features
    feature_cols = ['cgpa', 'internships', 'projects', 'communication', 'coding_score', 'aptitude_score']
    X = df[feature_cols]
    y = df['placement']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"\n📈 Training set: {len(X_train)} samples")
    print(f"📉 Test set: {len(X_test)} samples")
    
    # Define models
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        ),
        'Logistic Regression': LogisticRegression(
            max_iter=1000,
            random_state=42
        ),
        'SVM': SVC(
            kernel='rbf',
            probability=True,
            random_state=42
        ),
        'Decision Tree': DecisionTreeClassifier(
            max_depth=10,
            min_samples_split=5,
            random_state=42
        ),
        'AdaBoost': AdaBoostClassifier(
            n_estimators=100,
            random_state=42
        )
    }
    
    # Train and evaluate models
    results = []
    best_model = None
    best_score = 0
    
    print("\n🤖 Training and evaluating models...\n")
    
    for name, model in models.items():
        print(f"Training {name}...")
        
        # Use scaled data for models that benefit from it
        if name in ['Logistic Regression', 'SVM']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)
        
        # Cross-validation
        if name in ['Logistic Regression', 'SVM']:
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
        else:
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        results.append({
            'Model': name,
            'Accuracy': accuracy,
            'AUC': auc,
            'CV Mean': cv_scores.mean(),
            'CV Std': cv_scores.std()
        })
        
        print(f"  ✓ Accuracy: {accuracy:.4f}")
        print(f"  ✓ AUC: {auc:.4f}")
        print(f"  ✓ CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})\n")
        
        # Track best model
        if accuracy > best_score:
            best_score = accuracy
            best_model = (name, model)
    
    # Display results
    results_df = pd.DataFrame(results).sort_values('Accuracy', ascending=False)
    print("\n📊 Model Comparison:")
    print(results_df.to_string(index=False))
    
    # Save best model
    print(f"\n🏆 Best Model: {best_model[0]} (Accuracy: {best_score:.4f})")
    
    model_dir = os.path.dirname(__file__)
    model_path = os.path.join(model_dir, 'placement_model.pkl')
    
    # Save the best model
    joblib.dump(best_model[1], model_path)
    print(f"💾 Best model saved to: {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"💾 Scaler saved to: {scaler_path}")
    
    # Save to ml_models directory
    alt_model_dir = os.path.join(os.path.dirname(model_dir), 'ml_models')
    if os.path.exists(alt_model_dir):
        alt_model_path = os.path.join(alt_model_dir, 'placement_class_model.joblib')
        joblib.dump(best_model[1], alt_model_path)
        print(f"💾 Model also saved to: {alt_model_path}")
    
    # Generate visualizations
    print("\n📈 Generating visualizations...")
    viz_dir = os.path.join(model_dir, 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)
    
    # Feature importance
    importance = plot_feature_importance(
        best_model[1],
        feature_cols,
        os.path.join(viz_dir, 'feature_importance.png')
    )
    if importance is not None:
        print("\n⭐ Feature Importance:")
        print(importance.to_string(index=False))
    
    # Confusion matrix
    if best_model[0] in ['Logistic Regression', 'SVM']:
        y_pred_best = best_model[1].predict(X_test_scaled)
        y_pred_proba_best = best_model[1].predict_proba(X_test_scaled)[:, 1]
    else:
        y_pred_best = best_model[1].predict(X_test)
        y_pred_proba_best = best_model[1].predict_proba(X_test)[:, 1]
    
    plot_confusion_matrix(
        y_test,
        y_pred_best,
        os.path.join(viz_dir, 'confusion_matrix.png')
    )
    
    # ROC curve
    plot_roc_curve(
        y_test,
        y_pred_proba_best,
        os.path.join(viz_dir, 'roc_curve.png')
    )
    
    print(f"📊 Visualizations saved to: {viz_dir}")
    
    # Detailed classification report
    print("\n📋 Detailed Classification Report:")
    print(classification_report(y_test, y_pred_best, target_names=['Not Placed', 'Placed']))
    
    print("\n🔢 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_best))
    
    print("\n" + "=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    
    return best_model[1], results_df


if __name__ == "__main__":
    train_and_compare_models()
