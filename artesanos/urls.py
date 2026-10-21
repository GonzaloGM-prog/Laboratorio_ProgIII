from django.urls import path
from . import views

app_name = 'artesanos'

urlpatterns = [
    path('solicitud/', views.solicitud, name='solicitud'),
]