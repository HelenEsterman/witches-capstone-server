from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from witchesapi.models import Avatar

class AvatarSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    def get_is_owner(self, obj):

        current_user_id = self.context['request'].user.id
        return any(current_user_id == witch.user_id for witch in obj.witch.all())

    class Meta:
        model = Avatar
        fields = ['id', 'avatar_url', 'is_owner']

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
