"""
Direct API test without authentication
"""
import requests
import json

# First, login to get token
login_url = "http://127.0.0.1:8000/api/auth/login/"
login_data = {
    "username": "student1",
    "password": "password123"
}

print("Logging in...")
try:
    response = requests.post(login_url, json=login_data)
    print(f"Login Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data['tokens']['access']
        print(f"Token obtained: {token[:20]}...")
        
        # Now test prediction
        predict_url = "http://127.0.0.1:8000/api/ml/predict/"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        predict_data = {
            "cgpa": 8.5,
            "internships": 2,
            "projects": 3,
            "communication": 8
        }
        
        print("\nMaking prediction...")
        print(f"Input: {predict_data}")
        
        pred_response = requests.post(predict_url, json=predict_data, headers=headers)
        print(f"\nPrediction Status: {pred_response.status_code}")
        print(f"Response: {json.dumps(pred_response.json(), indent=2)}")
        
    else:
        print(f"Login failed: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
