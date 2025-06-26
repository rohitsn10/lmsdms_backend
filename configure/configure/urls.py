"""
URL configuration for configure project.

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
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from dms_module.views import onlyoffice_callback


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('user_profile/',include('user_profile.urls')),
#     path('lms_module/',include('lms_module.urls')),
#     path('dms_module/',include('dms_module.urls')),
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/user_profile/', include('user_profile.urls')),
    path('api/lms_module/', include('lms_module.urls')),
    path('api/dms_module/', include('dms_module.urls')),

    path('dms_module/onlyoffice_callback', onlyoffice_callback),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
