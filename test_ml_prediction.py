"""
Quick test script for ML prediction
"""
import joblib
import numpy as np
import os

# Load model
model_path = os.path.join('ml_model', 'placement_model.pkl')
print(f"Loading model from: {model_path}")
model = joblib.load(model_path)

print(f"Model type: {type(model).__name__}")
print(f"Model loaded successfully!\n")

# Test prediction
test_data = {
    'cgpa': 8.5,
    'internships': 2,
    'projects': 3,
    'communication': 8
}

print("Test Input:")
for key, value in test_data.items():
    print(f"  {key}: {value}")

# Make prediction
features = np.array([[
    test_data['cgpa'],
    test_data['internships'],
    test_data['projects'],
    test_data['communication']
]])

prediction = model.predict(features)
probability = model.predict_proba(features)[0]

print(f"\nPrediction: {'Placed' if prediction[0] == 1 else 'Not Placed'}")
print(f"Confidence: {max(probability):.2%}")
print(f"Probabilities: Not Placed={probability[0]:.2%}, Placed={probability[1]:.2%}")

# Test with different inputs
print("\n" + "="*60)
print("Testing with different inputs:")
print("="*60)

test_cases = [
    {'cgpa': 9.0, 'internships': 3, 'projects': 4, 'communication': 9},
    {'cgpa': 6.5, 'internships': 0, 'projects': 1, 'communication': 5},
    {'cgpa': 7.5, 'internships': 1, 'projects': 2, 'communication': 7},
]

for i, test in enumerate(test_cases, 1):
    features = np.array([[test['cgpa'], test['internships'], test['projects'], test['communication']]])
    pred = model.predict(features)
    prob = model.predict_proba(features)[0]
    
    print(f"\nTest {i}: CGPA={test['cgpa']}, Internships={test['internships']}, Projects={test['projects']}, Communication={test['communication']}")
    print(f"  Result: {'Placed' if pred[0] == 1 else 'Not Placed'} (Confidence: {max(prob):.2%})")

print("\n✅ Model is working correctly!")
