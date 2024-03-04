from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from witchesapi.models import Witch, Avatar, WitchInventory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

class WitchUserViewSet(viewsets.ViewSet):
    # all user objects in database are set to variable 'queryset'
    queryset = User.objects.all()
    # this means no 'auth_token' needed to make HTTP requests to this viewset instance
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # create user object from request body data
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name']
            )
            # create witch object same time you create user obj from request body data
            witch = Witch.objects.create(
                user = user,
                avatar = Avatar.objects.get(pk=request.data["avatar"]),
                nickname = request.data.get('nickname'),
                coven = request.data.get('coven')
            )
            # create witch inventory same time that you create a witch
            WitchInventory.objects.create(
                witch = witch
            )
            # create token associated with user
            token, created = Token.objects.get_or_create(user=user)
            # return token in response body
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def user_login(self, request):
        # get username and password from request body
        email = request.data.get('username')
        password = request.data.get('password')

        # authenticate user by checking username and password against the `username` and `password` values of users already registered within the auth_user table
        user = authenticate(username=email, password=password)

        # if authenticate() returns true, return the user's auth token in the request body
        if user:
            token = Token.objects.get(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)