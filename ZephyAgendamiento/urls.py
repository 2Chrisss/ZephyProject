from django.urls import path
from .views import agendar_box

urlpatterns = [
    path('agendar/', agendar_box, name='agendar_box'),
]
