from django.contrib.auth import authenticate
from django.core import signing
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.viewsets import ModelViewSet

from .models import User, Ledger
from .serializers import UserSerializer, LedgerSerializer

class LedgerViewSet(ModelViewSet):
    queryset = Ledger.objects.all()
    serializer_class = LedgerSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
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
        serializer = self.get_serializer(data=duplicated_instance)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request.user)
        headers = self.get_success_headers(serializer.data)
        
        data = {
            'message': 'Duplication Success',
            'result': serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

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


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'login' or self.action == 'create':
            return [AllowAny(), ]
        return [IsAuthenticated(), ]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            data = {
                'message': 'Signup Success',
                'registered_user': serializer.data,
                'token': {
                    'access': access_token,
                    'refresh': refresh_token,
                },
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = self.serializer_class(data=request.data)

        user = authenticate(
            email=request.data.get('email'),
            password=request.data.get('password')
        )
        if user:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            data = {
                'message': 'Login Success',
                'logined_user': serializer.data,
                'token': {
                    'access': access_token,
                    'refresh': refresh_token,
                },
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @action(methods=['post'], detail=False)
    def logout(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {'message': 'Logout Success'}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            data = {
                'message' : 'Logout Failed',
                'error': str(error)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)