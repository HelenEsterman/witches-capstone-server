from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from witchesapi.models import WitchIngredient

class WitchIngredientSerializer(serializers.ModelSerializer):
#    TODO: is_owner, witch_id serializer, and type_id serializer
    
    class Meta:
        model = WitchIngredient
        fields = [ 'id', 'witch_id','type_id', 'label', 'healing_property']

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
