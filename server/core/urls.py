from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views.ledgerviewset import LedgerViewSet
from core.views.userviewset import UserViewSet

app_name = 'core'

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('ledgers', LedgerViewSet, basename='ledger')

urlpatterns = [
    path('api/v0/', include(router.urls)),    
]