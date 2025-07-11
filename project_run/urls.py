"""
URL configuration for project_run project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from app_run.views import RunStartAPIView, RunStopAPIView, company_details, UserViewSet, RunViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company_details/', company_details),
    path('api/runs/', RunViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/runs/<int:pk>/', RunViewSet.as_view({'get': 'retrieve'})),
    path('api/users/', UserViewSet.as_view({'get': 'list'})),
    path('api/runs/<int:pk>/start/', RunStartAPIView.as_view()),
    path('api/runs/<int:pk>/stop/', RunStopAPIView.as_view()),
]