from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'core'

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('ledgers', views.LedgerViewSet, basename='ledger')

urlpatterns = [
    path('api/v0/', include(router.urls)),    
]