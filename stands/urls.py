from django.urls import path
from . import views

app_name = 'stands'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('agregar/', views.agregar, name='agregar'),
    path('<int:pk>/eliminar/', views.eliminar, name='eliminar'),
]
