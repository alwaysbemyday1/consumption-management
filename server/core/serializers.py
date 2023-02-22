from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User, Ledger

class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_admin', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, request):
        try:
            user = super().save()
            user.email = self.validated_data['email']
            user.set_password(self.validated_data['password'])
            user.save()
        except ValidationError as err:
            raise ValidationError(err)
        return user