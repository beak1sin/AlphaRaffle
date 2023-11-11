"""autodraw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from django.conf import settings



urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'',include('draw.urls')),
    path('',include('pwa.urls')),
] 

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),

            # For django versions before 2.0:
            # url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns


# 404 error
# from draw.views import customHandler404
# handler404 = customHandler404.as_view()

# from draw.views import customHandler500
# handler500 = customHandler500.as_view()
# from django.conf.urls import handler404
# handler404 = 'draw.views.custom_404'
# urls.py
# from django.conf.urls import handler404, handler500

# handler404 = 'draw.views.custom_404'
# handler500 = 'draw.views.custom_500'