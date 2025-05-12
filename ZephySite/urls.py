from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ZephyReportes.urls')), 
    path('zephy_estadisticas/', include('ZephyEstadisticas.urls')),  # Aquí debes incluir tus URLs de la app

]