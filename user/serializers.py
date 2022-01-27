from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ClientRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('phone', 'email', 'username', 'password1', 'password2')

    def validate(self, attrs):

        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"رمز عبور": "فیلدهای رمز عبور مطابقت نداشتند."})

        return attrs

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            is_client=True,
        )

        user.set_password(validated_data['password1'])
        user.save()
        return user
        
class GetTokenForLoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super(GetTokenForLoginSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'email', 'username', 'image', 'first_name', 'last_name')

class GenerateOtpLoginSerializer(serializers.Serializer):
    phone= serializers.CharField(write_only=True, required=True)


class LoginUserWithOtpSerializer(serializers.Serializer):
    phone= serializers.CharField(write_only=True, required=True)
    otp = serializers.CharField(write_only=True, required=True)