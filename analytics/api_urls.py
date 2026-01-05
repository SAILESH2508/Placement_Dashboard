from django.urls import path
from .api_views import DeptStatsView, DailyStatsView, PredictMLView, ModelMetricsView, RetrainModelView

urlpatterns = [
    path('dept/', DeptStatsView.as_view(), name='dept_stats'),
    path('daily/', DailyStatsView.as_view(), name='daily_stats'),
    path('predict/', PredictMLView.as_view(), name='predict_ml'),
    path('metrics/', ModelMetricsView.as_view(), name='model_metrics'),
    path('retrain/', RetrainModelView.as_view(), name='retrain_model'),
]
