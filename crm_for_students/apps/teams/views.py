# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .models import CustomUser
from .serializers import UserCRUDSerializer


class UserCreateView(APIView):
    @extend_schema(
        request=UserCRUDSerializer,
        responses={201: UserCRUDSerializer},
        description="Create a new user"
    )
    def post(self, request):
        """
        Create a new user.
        """
        serializer = UserCRUDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    @extend_schema(
        responses={200: UserCRUDSerializer},
        description="Retrieve a user by ID"
    )
    def get_object(self, pk):
        return get_object_or_404(CustomUser, pk=pk)

    @extend_schema(
        responses={200: UserCRUDSerializer},
        description="Retrieve a user by ID"
    )
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserCRUDSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        request=UserCRUDSerializer,
        responses={200: UserCRUDSerializer},
        description="Update a user by ID"
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserCRUDSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        responses={204: None},
        description="Delete a user by ID"
    )
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
