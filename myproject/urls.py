"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from core.views import index, welcome, register


class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'options']
    
    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        from django.shortcuts import redirect
        return redirect('/')
    
    def post(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        from django.shortcuts import redirect
        return redirect('/')


urlpatterns = [
    path('admin/', admin.site.urls),
    # Trang đầu tiên: trang chào mừng
    path('', welcome, name='welcome'),
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('todo/', index, name='todo'),  # Trang todo - yêu cầu login
]
