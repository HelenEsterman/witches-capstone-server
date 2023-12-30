from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from witchesapi.models import IngredientType, WitchInventoryIngredient

class IngredientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientType
        fields = ['id', 'label']

class IngredientTypeViewSet(viewsets.ViewSet):

    def list(self, request):
        types = IngredientType.objects.all()
        serializer = IngredientTypeSerializer(types, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            type = IngredientType.objects.get(pk=pk)
            serializer = IngredientTypeSerializer(type, many=False, context={'request': request})
            return Response(serializer.data)

        except IngredientType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
