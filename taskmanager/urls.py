from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, CategoryViewSet
from accounts.views import register_view, login_view

# Create a central REST router engine and register viewsets
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # Admin Interface Path
    path('admin/', admin.site.urls),
    
    # Custom Authentication Endpoint Handles
    path('api/auth/register/', register_view, name='register'),
    path('api/auth/login/', login_view, name='login'),
    
    # Core API Operational Hub Mappings
    path('api/', include(router.urls)),
]