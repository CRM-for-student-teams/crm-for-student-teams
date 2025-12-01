from rest_framework.serializers import (
    ModelSerializer, 
    CharField,
    ValidationError,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(ModelSerializer):
    """
    Serializer for user detail
    """
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "inserted_at"]
        read_only_fields = ["id", "inserted_at"]

    
class UserRegistrationSerializer(ModelSerializer):
    """
    Serializer for user registration
    """
    password = CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )
    password_confirm = CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["email", "password", "password_confirm", "full_name"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise ValidationError(
                {"password": "Password fields should be match"}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer
    """
    username_field = "email"
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = UserSerializer(self.user).data

        return data