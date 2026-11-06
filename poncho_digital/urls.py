from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from usuarios.forms import IngresoForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base/home.html'), name='home'),
    path('contacto/', TemplateView.as_view(template_name='base/contacto.html'), name='contacto'),
    path('ingresar/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=IngresoForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path('salir/', auth_views.LogoutView.as_view(), name='logout'),
    path('artesanos/', include('artesanos.urls', namespace='artesanos')),
    path('productos/', include('productos.urls', namespace='productos')),
    path('stands/', include('stands.urls', namespace='stands')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
