from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
import joblib
import numpy as np
import pandas as pd
import os
import logging
from datetime import datetime
import warnings

logger = logging.getLogger(__name__)

# Suppress sklearn feature name warnings
warnings.filterwarnings('ignore', message='X does not have valid feature names')

# Cache the model and scaler to avoid loading on every request
_model_cache = {}

def load_model():
    """Load ML model with caching"""
    if 'placement_model' not in _model_cache:
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'placement_model.pkl')
            if not os.path.exists(model_path):
                logger.error(f"Model file not found at: {model_path}")
                return None
            _model_cache['placement_model'] = joblib.load(model_path)
            logger.info("ML model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return None
    return _model_cache['placement_model']

def load_scaler():
    """Load scaler if available"""
    if 'scaler' not in _model_cache:
        try:
            scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
            if os.path.exists(scaler_path):
                _model_cache['scaler'] = joblib.load(scaler_path)
                logger.info("Scaler loaded successfully")
            else:
                _model_cache['scaler'] = None
        except Exception as e:
            logger.error(f"Error loading scaler: {str(e)}")
            _model_cache['scaler'] = None
    return _model_cache['scaler']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_placement(request):
    """
    Predict placement probability based on student features
    
    Expected input:
    {
        "cgpa": float (0-10),
        "internships": int (0+),
        "projects": int (0+),
        "communication": int (1-10)
    }
    """
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['cgpa', 'internships', 'projects', 'communication']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Parse and validate input
        try:
            cgpa = float(data.get('cgpa'))
            internships = int(data.get('internships'))
            projects = int(data.get('projects'))
            communication = int(data.get('communication'))
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid data types. Ensure cgpa is a number, and others are integers."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate ranges
        if not (0 <= cgpa <= 10):
            return Response(
                {"error": "CGPA must be between 0 and 10"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if internships < 0 or projects < 0:
            return Response(
                {"error": "Internships and projects cannot be negative"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not (1 <= communication <= 10):
            return Response(
                {"error": "Communication score must be between 1 and 10"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Load model
        model = load_model()
        if model is None:
            return Response(
                {"error": "ML model not available. Please train the model first."}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Make prediction using DataFrame with feature names
        feature_names = ['cgpa', 'internships', 'projects', 'communication']
        features = pd.DataFrame([[cgpa, internships, projects, communication]], columns=feature_names)
        prediction = model.predict(features)
        probability = model.predict_proba(features)[0] if hasattr(model, 'predict_proba') else None

        result = {
            "prediction": "Placed" if prediction[0] == 1 else "Not Placed",
            "confidence": float(max(probability)) if probability is not None else None,
            "input_features": {
                "cgpa": cgpa,
                "internships": internships,
                "projects": projects,
                "communication": communication
            }
        }

        logger.info(f"Prediction made: {result['prediction']} with confidence {result['confidence']}")
        return Response(result)

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Prediction error: {str(e)}\n{error_details}")
        print(f"ERROR in predict_placement: {str(e)}")
        print(error_details)
        return Response(
            {"error": f"An error occurred during prediction: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def batch_predict(request):
    """
    Batch prediction for multiple students
    
    Expected input:
    {
        "students": [
            {"cgpa": 8.5, "internships": 2, "projects": 3, "communication": 8},
            {"cgpa": 7.0, "internships": 1, "projects": 2, "communication": 6},
            ...
        ]
    }
    """
    try:
        students = request.data.get('students', [])
        
        if not students or not isinstance(students, list):
            return Response(
                {"error": "Invalid input. Expected 'students' array."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        model = load_model()
        if model is None:
            return Response(
                {"error": "ML model not available"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        results = []
        for idx, student in enumerate(students):
            try:
                cgpa = float(student.get('cgpa', 0))
                internships = int(student.get('internships', 0))
                projects = int(student.get('projects', 0))
                communication = int(student.get('communication', 0))
                
                # Validate ranges
                if not (0 <= cgpa <= 10) or internships < 0 or projects < 0 or not (1 <= communication <= 10):
                    results.append({
                        "index": idx,
                        "error": "Invalid data ranges",
                        "prediction": None
                    })
                    continue
                
                feature_names = ['cgpa', 'internships', 'projects', 'communication']
                features = pd.DataFrame([[cgpa, internships, projects, communication]], columns=feature_names)
                prediction = model.predict(features)
                probability = model.predict_proba(features)[0] if hasattr(model, 'predict_proba') else None
                
                results.append({
                    "index": idx,
                    "prediction": "Placed" if prediction[0] == 1 else "Not Placed",
                    "confidence": float(max(probability)) if probability is not None else None,
                    "input": {
                        "cgpa": cgpa,
                        "internships": internships,
                        "projects": projects,
                        "communication": communication
                    }
                })
            except Exception as e:
                results.append({
                    "index": idx,
                    "error": str(e),
                    "prediction": None
                })
        
        return Response({"results": results})
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return Response(
            {"error": "An error occurred during batch prediction"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def model_info(request):
    """
    Get information about the ML model
    """
    try:
        model = load_model()
        
        if model is None:
            return Response(
                {"error": "ML model not available"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        info = {
            "model_type": type(model).__name__,
            "features": ["cgpa", "internships", "projects", "communication"],
            "feature_ranges": {
                "cgpa": "0-10",
                "internships": "0+",
                "projects": "0+",
                "communication": "1-10"
            },
            "status": "active",
            "last_updated": "2025-11-30",
        }
        
        # Add feature importance if available
        if hasattr(model, 'feature_importances_'):
            features = ["cgpa", "internships", "projects", "communication"]
            importance = dict(zip(features, model.feature_importances_.tolist()))
            info["feature_importance"] = importance
        
        # Add model parameters if available
        if hasattr(model, 'get_params'):
            info["parameters"] = {
                k: str(v) for k, v in model.get_params().items()
                if not k.startswith('_')
            }
        
        return Response(info)
        
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        return Response(
            {"error": "An error occurred while fetching model info"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prediction_stats(request):
    """
    Get statistics about predictions made
    """
    try:
        # This is a placeholder - in production, you'd track predictions in database
        stats = {
            "total_predictions": 0,
            "placed_predictions": 0,
            "not_placed_predictions": 0,
            "average_confidence": 0.0,
            "last_prediction": None,
            "message": "Prediction tracking not yet implemented. This is a demo response."
        }
        
        return Response(stats)
        
    except Exception as e:
        logger.error(f"Prediction stats error: {str(e)}")
        return Response(
            {"error": "An error occurred while fetching stats"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

