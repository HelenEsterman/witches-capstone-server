from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from witchesapi.models import WitchIngredient, IngredientType, Witch, Avatar


class IngredientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientType
        fields = ['id', 'label']

class WitchAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'avatar_url']

class WitchSerializer(serializers.ModelSerializer):
    avatar = WitchAvatarSerializer(many=False)
    class Meta:
        model = Witch
        fields = ['id', 'avatar']

class WitchIngredientSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    type = IngredientTypeSerializer(many=False)
    witch = WitchSerializer(many=False)
    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.witch.user
    
    class Meta:
        model = WitchIngredient
        fields = [ 'id', 'witch','type', 'label', 'healing_property', 'is_owner']

class WitchIngredientViewSet(viewsets.ViewSet):

    def list(self, request):
        witchesIngredients = WitchIngredient.objects.all()
        serializer = WitchIngredientSerializer(witchesIngredients, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            witchesIngredient = WitchIngredient.objects.get(pk=pk)
            serializer = WitchIngredientSerializer(witchesIngredient, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except WitchIngredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
