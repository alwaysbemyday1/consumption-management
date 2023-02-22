from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer


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