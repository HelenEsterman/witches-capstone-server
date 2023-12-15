from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from witchesapi.models import Avatar

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'avatar_url']

class AvatarViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]

    def list(self, request):
        avatars = Avatar.objects.all()
        serializer = AvatarSerializer(avatars, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            avatar = Avatar.objects.get(pk=pk)
            serializer = AvatarSerializer(avatar, many=False, context={'request': request})
            return Response(serializer.data)

        except Avatar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
