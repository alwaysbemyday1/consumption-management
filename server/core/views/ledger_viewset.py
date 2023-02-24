from django.core import signing
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Ledger
from core.serializers.ledger_serializer import LedgerSerializer

class LedgerViewSet(ModelViewSet):
    queryset = Ledger.objects.all()
    serializer_class = LedgerSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, user)
        headers = self.get_success_headers(serializer.data)
        data = {
            'message': 'Ledger creation Success',
            'results': serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, user):
        serializer.save(user=user)
        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset().filter(user=user)
        count = queryset.count()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'count': count,
            'results': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='duplication')
    def duplicate(self, request, pk):
        instance = self.get_object()
        duplicated_instance = {
            'amount': instance.amount,
            'memo': instance.memo
        }
        serializer = self.serializer_class(data=duplicated_instance)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request.user)
        headers = self.get_success_headers(serializer.data)
        
        data = {
            'message': 'Duplication Success',
            'result': serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def generate_temp_url(self, data=None):
        return reverse('core:ledger-temp', args=[signing.dumps(data)])

    @action(methods=['get'], detail=True, url_path='temp', url_name='temp')
    def share_temp_url(self, request, pk):
        instance = self.get_object()
        serilizer = self.get_serializer(instance)
        serilized_data = serilizer.data
        signed_url = self.generate_temp_url(serilized_data)
        data = {
            'message': 'Creating Temporary URL Success',
            'result': f'http://127.0.0.1:8000{signed_url}'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path=r'(?P<signed_data>[^/.]+)/temp')
    def view_temp_url(self, request, signed_data):
        URL_MAX_AGE_SECONDS = 1800
        try:
            decoded_data = signing.loads(signed_data, max_age=URL_MAX_AGE_SECONDS)
        except signing.BadSignature:
            # triggers an ResponseBadRequest (status 400) when DEBUG is False
            raise SuspiciousOperation('invalid signature')
        data = {
            'message': 'Viewing Temporary URL Success',
            'result': f'{decoded_data}'
        }
        return Response(data, status=status.HTTP_200_OK)