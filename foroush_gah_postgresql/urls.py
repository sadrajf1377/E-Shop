"""
URL configuration for foroush_gah_postgresql project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import django.conf.urls

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from foroush_gah_postgresql import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('product_module.urls'))
    ,path('register_login/',include('register_login.urls'))
    ,path('users/',include('user_Module.urls'))
    ,path('comments/',include('comments_module.urls'))
    ,path('order/',include('order_module.urls')),
    path('admin_module/',include('admin_module.urls')),
    path('ticket_module/',include('ticket_module.urls')),
    path('notification_module/',include('notification_module.urls'))

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
