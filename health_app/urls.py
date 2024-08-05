# health_app/urls.py
from django.urls import path
from .views import SleepConditionAPIView, Steps1ConditionAPIView, Steps2ConditionAPIView

urlpatterns = [
    path('sleep-condition/', SleepConditionAPIView.as_view(), name='sleep-condition'),
    path('steps1-condition/', Steps1ConditionAPIView.as_view(), name='steps1-condition'),
    path('steps2-condition/', Steps2ConditionAPIView.as_view(), name='steps2-condition'),
]
