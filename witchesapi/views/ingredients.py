from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from witchesapi.models import Ingredient, IngredientType

# define a serializer for the type key on the ingredients object
class IngredientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientType
        fields = ['id', 'label']

# define a serializer for ingredient objects
class IngredientSerializer(serializers.ModelSerializer):
    # assign type field to the correct serializer
    type = IngredientTypeSerializer(many=False)
   
    class Meta:
        model = Ingredient
        fields = [ 'id', 'type', 'label', 'healing_property']

class IngredientViewSet(viewsets.ViewSet):

    def list(self, request):
        # grab all the ingredient objects from the database
        ingredients = Ingredient.objects.all()
        # serialize those objects into json format
        serializer = IngredientSerializer(ingredients, many=True, context={'request': request})
        # return serialized data in response body
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            # grab the ingredient object from the database with the specific PK
            ingredient = Ingredient.objects.get(pk=pk)
            # serialize the object into json format
            serializer = IngredientSerializer(ingredient, many=False, context={'request': request})
            # return serialized data in response body
            return Response(serializer.data)
        # error handle if ingredient with specific Pk doesn't exist
        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
