from django.urls import path
from .views import predict_placement, batch_predict, model_info, prediction_stats

urlpatterns = [
    path('predict/', predict_placement, name='predict_placement'),
    path('batch-predict/', batch_predict, name='batch_predict'),
    path('model-info/', model_info, name='model_info'),
    path('stats/', prediction_stats, name='prediction_stats'),
]
