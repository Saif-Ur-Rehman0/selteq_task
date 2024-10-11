"""
URL configuration for selteq_task project.

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
from django.urls import path
from TaskApp import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/tasks/', views.create_task, name='create_task'),
    path('api/tasks/all/', views.get_all_tasks, name='get_all_tasks'),    
    path('api/tasks/<int:task_id>/', views.retrieve_task, name='retrieve_task'),
    path('api/tasks/<int:task_id>/update/', views.update_task_title, name='update_task_title'),
    path('api/tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('trigger-tasks/', views.trigger_print_tasks, name='trigger_tasks'),
]
