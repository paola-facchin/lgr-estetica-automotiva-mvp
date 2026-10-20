from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from core.health import health

urlpatterns = [
    path('health/', health, name='health'),
    path('admin/', admin.site.urls),
    path('contas/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('contas/sair/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('core.urls')),
]
