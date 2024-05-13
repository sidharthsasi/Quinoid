# serializers.py
from rest_framework import serializers
from .models import Account
from rest_framework_simplejwt.tokens import RefreshToken



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Account
        fields = ['first_name','last_name','username','email', 'password']

    def create(self, validated_data):
        user = Account.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = Account.objects.filter(email=email).first()

            if user and user.check_password(password):
                return {'user': user}
            else:
                raise serializers.ValidationError("Incorrect email or password.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
