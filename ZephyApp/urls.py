from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('box/', views.box_list, name='box_list'),  

    path('box/<int:box_id>/cambiar_estado/', views.cambiar_estado_box, name='cambiar_estado_box'),

]