from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('agregar/', views.agregar, name='agregar'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar, name='eliminar'),
    path('reporte/', views.reporte_productos, name='reporte'),
    path('reporte/artesano/<int:pk>/', views.reporte_artesano, name='reporte_artesano'),
]
