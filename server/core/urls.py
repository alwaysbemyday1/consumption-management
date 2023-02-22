from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('ledgers', views.LedgerViewSet)

urlpatterns = [
    path('api/v0/', include(router.urls)),    
]