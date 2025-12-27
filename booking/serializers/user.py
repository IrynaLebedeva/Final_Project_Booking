import re
from typing import Any

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from booking.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'age',
                  'role',
                  'date_joined',
                  'is_active')
        read_only_fields = ('id', 'date_joined', 'is_active')

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'password',
            're_password',
            'role',
        )

    def validate(self, attrs: dict[str, Any]):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        password = attrs.get('password')
        re_password = attrs.pop('re_password', None) #!
        email = attrs.get('email')

        re_pattern = r"^[a-zA-Z]+$"

        if not re.match(re_pattern, first_name):
            raise serializers.ValidationError('First and last name must contain only letters.')
        if not re.match(re_pattern, last_name):
            raise serializers.ValidationError('First and last name must contain only letters.')
        if not password:
            raise serializers.ValidationError('Password is required.')
        if not re_password:
            raise serializers.ValidationError('Confirm password is required.')

        validate_password(password)
        if password != re_password:
            raise serializers.ValidationError('Passwords do not match.')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists.')

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user