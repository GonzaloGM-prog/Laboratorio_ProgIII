from django.urls import path
from . import views

app_name = 'artesanos'

urlpatterns = [
    path('solicitud/', views.solicitud, name='solicitud'),
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('solicitudes/<int:pk>/<str:accion>/', views.resolver_solicitud, name='resolver'),
]
