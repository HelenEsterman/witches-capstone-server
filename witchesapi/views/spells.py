from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from witchesapi.models import Spell, SpellIngredient

class SpellIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellIngredient
        fields = ['id', 'label']

class SpellSerializer(serializers.ModelSerializer):
    ingredients = SpellIngredientSerializer(many=True)
    
    class Meta:
        model = Spell
        fields = [ 'id', 'name', 'intention', 'chant', 'repeat_chant', 'when_most_powerful', 'location', 'other_instructions', 'favorite', 'ingredients']

class SpellViewSet(viewsets.ViewSet):

    def list(self, request):
        spells = Spell.objects.all()
        serializer = SpellSerializer(spells, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            spell = Spell.objects.get(pk=pk)
            serializer = SpellSerializer(spell, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Spell.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
