from django.urls import path
from core.views import DetectMaskView

urlpatterns = [
    path('', DetectMaskView.as_view(), name='detect-mask'),
]
