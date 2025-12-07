# core/api_ml.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ml_models import predict_single, load_models
from rest_framework import serializers
import pandas as pd

class PredictionInputSerializer(serializers.Serializer):
    branch = serializers.CharField(max_length=50)
    cgpa = serializers.FloatField()
    year = serializers.IntegerField()

class PredictSingleView(APIView):
    """
    POST /api/predict_single/  JSON: {branch, cgpa, year}
    Response: placement_probability, predicted_package_lpa
    """
    def post(self, request):
        serializer = PredictionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            res = predict_single(data)
        except FileNotFoundError as e:
            return Response({'detail': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(res, status=status.HTTP_200_OK)

class PredictBatchView(APIView):
    """
    POST /api/predict_batch/  JSON: {"samples": [ {branch,cgpa,year}, ... ]}
    """
    def post(self, request):
        samples = request.data.get('samples')
        if not isinstance(samples, list):
            return Response({'detail': 'samples must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PredictionInputSerializer(data=samples, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        valid = serializer.validated_data
        # Use ml_models.load_models to transform and batch predict
        try:
            preprocessor, clf, reg = load_models()
        except FileNotFoundError as e:
            return Response({'detail': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        df = pd.DataFrame(valid)
        X_trans = preprocessor.transform(df)
        probs = clf.predict_proba(X_trans)[:, 1]
        pkgs = reg.predict(X_trans)
        out = []
        for i, s in enumerate(valid):
            out.append({
                'input': s,
                'placement_probability': float(probs[i]),
                'predicted_package_lpa': float(pkgs[i])
            })
        return Response({'predictions': out}, status=status.HTTP_200_OK)
