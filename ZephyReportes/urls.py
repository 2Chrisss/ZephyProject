from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('box/', views.box_list, name='box_list'),
    path('box/<int:box_id>/', views.box_detalle, name='box_detalle'),


]