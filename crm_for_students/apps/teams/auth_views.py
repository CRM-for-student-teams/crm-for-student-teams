# Django modules
from django.contrib.auth import get_user_model

# DRF modules
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
)
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer
from rest_framework import serializers

# Project modules
from .auth_serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)


User = get_user_model()


@extend_schema(
    operation_id="auth_login",
    summary="User login",
    description="""Authenticate a user and obtain JWT access and refresh tokens.
    
    **Authentication Flow:**
    1. Send email and password
    2. Receive access token (short-lived) and refresh token (long-lived)
    3. Use access token in Authorization header: `Bearer <access_token>`
    4. Refresh access token using refresh token when expired
    
    **Token Lifetimes:**
    - Access token: 15 minutes
    - Refresh token: 7 days
    """,
    tags=["Authentication"],
    request=CustomTokenObtainPairSerializer,
    responses={
        HTTP_200_OK: inline_serializer(
            name="TokenResponse",
            fields={
                "access": serializers.CharField(),
                "refresh": serializers.CharField(),
                "user": UserSerializer(),
            },
        ),
        HTTP_400_BAD_REQUEST: inline_serializer(
            name="LoginError",
            fields={
                "detail": serializers.CharField(),
            },
        ),
    },
    examples=[
        OpenApiExample(
            "Login Request",
            value={"email": "user@example.com", "password": "securePassword123"},
            request_only=True,
        ),
        OpenApiExample(
            "Success Response",
            value={
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "full_name": "John Doe",
                    "role": "student",
                },
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Invalid Credentials",
            value={"detail": "No active account found with the given credentials"},
            response_only=True,
            status_codes=["401"],
        ),
    ],
)
class CustomTokenPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view
    """

    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    operation_id="auth_register",
    summary="Register new user",
    description="""Create a new user account and receive authentication tokens.
    
    **Registration Process:**
    1. Provide email, password, and full name
    2. Account is created immediately
    3. JWT tokens are automatically generated
    4. User can start using the API right away
    
    **Password Requirements:**
    - Minimum 8 characters
    - Cannot be too similar to email or name
    - Cannot be entirely numeric
    - Cannot be a commonly used password
    """,
    tags=["Authentication"],
    request=UserRegistrationSerializer,
    responses={
        HTTP_201_CREATED: inline_serializer(
            name="RegisterResponse",
            fields={
                "user": UserSerializer(),
                "tokens": inline_serializer(
                    name="TokenPair",
                    fields={
                        "access": serializers.CharField(),
                        "refresh": serializers.CharField(),
                    },
                ),
            },
        ),
        HTTP_400_BAD_REQUEST: inline_serializer(
            name="RegisterError",
            fields={
                "email": serializers.ListField(child=serializers.CharField()),
                "password": serializers.ListField(child=serializers.CharField()),
                "full_name": serializers.ListField(child=serializers.CharField()),
            },
        ),
    },
    examples=[
        OpenApiExample(
            "Register Request",
            value={
                "email": "newuser@example.com",
                "password": "securePassword123",
                "full_name": "Jane Smith",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Success Response",
            value={
                "user": {
                    "id": 5,
                    "email": "newuser@example.com",
                    "full_name": "Jane Smith",
                    "role": "student",
                    "inserted_at": "2025-01-15T10:00:00Z",
                    "updated_at": "2025-01-15T10:00:00Z",
                },
                "tokens": {
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                },
            },
            response_only=True,
            status_codes=["201"],
        ),
        OpenApiExample(
            "Email Already Exists",
            value={"email": ["User with this email already exists."]},
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            "Weak Password",
            value={
                "password": [
                    "This password is too short. It must contain at least 8 characters.",
                    "This password is too common.",
                ]
            },
            response_only=True,
            status_codes=["400"],
        ),
    ],
)
class RegisterView(CreateAPIView):
    """
    User registration endpoint
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=HTTP_201_CREATED,
        )


@extend_schema(
    operation_id="auth_current_user",
    summary="Get current user",
    description="""Retrieve information about the currently authenticated user.
    
    **Usage:**
    - Requires valid JWT access token in Authorization header
    - Returns user profile information
    - Useful for verifying token validity and getting user details
    
    **Authorization Header Format:**
    ```
    Authorization: Bearer <your_access_token>
    ```
    """,
    tags=["Authentication"],
    responses={
        HTTP_200_OK: UserSerializer,
        401: inline_serializer(
            name="Unauthorized",
            fields={
                "detail": serializers.CharField(),
            },
        ),
    },
    examples=[
        OpenApiExample(
            "Current User Response",
            value={
                "id": 1,
                "email": "user@example.com",
                "full_name": "John Doe",
                "role": "student",
                "inserted_at": "2025-01-01T10:00:00Z",
                "updated_at": "2025-01-10T15:30:00Z",
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Invalid Token",
            value={"detail": "Given token not valid for any token type"},
            response_only=True,
            status_codes=["401"],
        ),
    ],
)
class CurrentUserView(RetrieveAPIView):
    """
    Ger current authenticated user info
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user


@extend_schema(
    operation_id="auth_logout",
    summary="User logout",
    description="""Logout by blacklisting the refresh token.
    
    **Logout Process:**
    1. Send the refresh token in the request body
    2. Token is added to blacklist
    3. Token can no longer be used to obtain new access tokens
    4. Client should delete stored tokens
    
    **Note:** The access token will remain valid until it expires (15 minutes).
    For immediate invalidation, implement token revocation on the client side.
    """,
    tags=["Authentication"],
    request=inline_serializer(
        name="LogoutRequest",
        fields={
            "refresh": serializers.CharField(
                help_text="The refresh token to blacklist"
            ),
        },
    ),
    responses={
        HTTP_200_OK: inline_serializer(
            name="LogoutSuccess",
            fields={
                "message": serializers.CharField(),
            },
        ),
        HTTP_400_BAD_REQUEST: inline_serializer(
            name="LogoutError",
            fields={
                "error": serializers.CharField(),
            },
        ),
    },
    examples=[
        OpenApiExample(
            "Logout Request",
            value={"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."},
            request_only=True,
        ),
        OpenApiExample(
            "Success Response",
            value={"message": "Successfully log out"},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Missing Token",
            value={"error": "Refresh token is required"},
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            "Invalid Token",
            value={"error": "Token is invalid or expired"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)
class LogoutView(GenericAPIView):
    """
    Logout by blacklisting the refresh token
    """

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"}, status=HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully log out"}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
