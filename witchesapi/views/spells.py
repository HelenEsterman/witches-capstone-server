from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from witchesapi.models import Spell, SpellIngredient, Equipment, WitchInventoryIngredient
from .ingredients import IngredientSerializer

class SpellIngredientSerializer(serializers.ModelSerializer):
    # serialize ingredient key on spellIngredient joint table obj
    ingredient = IngredientSerializer(many=False)   

    # ad hoc property is_owned to determine if spell ingredient is in witches inventory
    is_owned = serializers.SerializerMethodField()

    # define ad hoc method
    def get_is_owned(self, obj):
        # get request payload to get authenticated current user
        request = self.context.get('request')
        # get all ingredients associated with spell
        spell_ingredients = SpellIngredient.objects.filter(spell_id=obj.spell_id)
        # get all of the current user's ingredients in their inventory
        witches_inventory_ingredients = WitchInventoryIngredient.objects.filter(inventory_id=request.auth.user.id)
        # create a dictionary to store the ownership status of each ingredient (memoization)
        ingredient_status = {}
        # iterate through both the ingredients for the spell and the ingredients owned by the current user and compare
        for ingredient in spell_ingredients:
            for witch_ingredient in witches_inventory_ingredients:
                if ingredient.ingredient_id == witch_ingredient.ingredient_id:
                    ingredient_status[ingredient.ingredient_id] = True
        return ingredient_status.get(obj.ingredient_id, False)
          
    class Meta:
        model = SpellIngredient
        # define specified fields for SpellIngredient serializer
        fields = ['id', 'measurement', 'ingredient', 'is_owned']

class SpellEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'label']

class SpellSerializer(serializers.ModelSerializer): 
    # use the related_name naming convention on the spells key of the SpellIngredient joint table object this will embed the SpellIngredient ingredients AND their measurements because we defined that in the SpellIngredientSerializer
    spells_ingredients = SpellIngredientSerializer(many=True)
    equipment = SpellEquipmentSerializer(many=True)
    class Meta:
        model = Spell
        #  must use related_name naming in fields as well
        fields = [ 'id', 'name', 'intention', 'chant', 'repeat_chant', 'when_most_powerful', 'location', 'instructions', 'additional_info','favorite', 'spells_ingredients', 'equipment']

class SpellViewSet(viewsets.ViewSet):

    def list(self, request):
        # grab all the spell objects from the database
        spells = Spell.objects.all()
        # serialize those objects into json format
        serializer = SpellSerializer(spells, many=True, context={'request': request})
        # return serialized data in response body (no status code needed because django default is 200 ok)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            # grab the spell object from the database with the specific PK
            spell = Spell.objects.get(pk=pk)
            # serialize the object into json format
            serializer = SpellSerializer(spell, many=False, context={'request': request})
             # return serialized data in response body (no status code needed because django default is 200 ok)
            return Response(serializer.data)
            # error handle if spell with specific Pk doesn't exist
        except Spell.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
