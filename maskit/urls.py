"""maskit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from maskitapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('index',views.home),
    path('manage',views.manage),
    path('login',views.loginview),
    path('signup',views.registerview),
    path('logout',views.logoutview),
    path('account',views.account),
    path('add',views.add),
    path('edit',views.edit),
    path('gotoedit',views.gotoedit),
    path('history',views.history),
    path('livefeed',views.livefeed),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
