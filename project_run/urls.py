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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from app_run.views import my_function_based_view, RunViewSet, UserViewSet, RunUserViewSet, RunStartViewSet, \
    RunStopViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/runs', RunUserViewSet)
router.register('api/users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company_details/', my_function_based_view),
    path('api/runs/<int:id>/start/', RunStartViewSet.as_view()),
    path('api/runs/<int:id>/stop/', RunStopViewSet.as_view()),
    path('', include(router.urls))
]
