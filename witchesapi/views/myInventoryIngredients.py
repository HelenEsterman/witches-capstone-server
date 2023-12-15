from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from witchesapi.models import WitchInventoryIngredient, WitchInventory, Witch, Ingredient
from .avatars import AvatarSerializer
from .ingredients import IngredientSerializer
from datetime import datetime

# define serializer for 'witch' key on 'inventory' key on obj
class WitchSerializer(serializers.ModelSerializer):
    # serialize avatar obj by importing AvatarSerializer
    avatar = AvatarSerializer(many=False)
    class Meta:
        model = Witch
        fields = ['user', 'avatar']
# define serializer for 'inventory' key on obj
class InventorySerializer(serializers.ModelSerializer):
    # serialize witch obj
    witch = WitchSerializer(many=False)
    class Meta:
        model = WitchInventory
        fields = ['witch']

# define a serializer for the inventory ingredients
class MyInventoryIngredientSerializer(serializers.ModelSerializer):
    # serialize inventory obj
    inventory = InventorySerializer(many=False)
    # serialize ingredient obj by importing IngredientSerializer
    ingredient = IngredientSerializer(many=False)
    class Meta:
        model = WitchInventoryIngredient
        fields = ['id','inventory','ingredient', 'quantity', 'unit', 'added_on']

class WitchInventoryIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = WitchInventoryIngredient
        fields = ['id', 'ingredient', 'quantity', 'unit', 'added_on']


class MyInventoryIngredientViewSet(viewsets.ViewSet):

    def list(self, request):
        # grab only the ingredients that exist in 'my' (current user) inventory
        myInventoryIngredients = WitchInventoryIngredient.objects.filter(inventory_id=request.auth.user.id)
        serializer = MyInventoryIngredientSerializer(myInventoryIngredients, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            # grab the ingredient object from the database with the specific PK that is owned by 'me' (current user)
            myInventoryIngredient = WitchInventoryIngredient.objects.get(pk=pk, inventory_id=request.auth.user.id)
            # serialize the object into json format
            serializer = MyInventoryIngredientSerializer(myInventoryIngredient, many=False, context={'request': request})
            # return serialized data in response body
            return Response(serializer.data)
        # error handle if ingredient with specific Pk doesn't exist
        except WitchInventoryIngredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        # get data values from request body
        quantity = request.data['quantity']
        unit = request.data['unit']

        # instantiate a witchInventoryIngredient object to have a row PK to work with
        witchInventoryIngredient = WitchInventoryIngredient.objects.create(
            quantity = quantity,
            unit = unit,
            ingredient = Ingredient.objects.get(pk=request.data["ingredient"]),
            inventory = WitchInventory.objects.get(pk=request.auth.user.id),
        )
        # serialize data into json format to be processed
        serializer = MyInventoryIngredientSerializer(witchInventoryIngredient, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        try:
            # grab the object with pk from client request URL
            witchInventoryIngredient = WitchInventoryIngredient.objects.get(pk=pk)

            # check that the current user trying to edit IS owner of ingredient
            if witchInventoryIngredient.inventory_id == request.auth.user.id:
                
                # serialize the request body data and assign it to variable
                serializer = WitchInventoryIngredientSerializer(data=request.data)

                # checking to see if the data was properly serialized, meaning that all fields defined within serializer, were sent from client within request body
                if serializer.is_valid():
                    witchInventoryIngredient.ingredient = serializer.validated_data['ingredient']
                    witchInventoryIngredient.quantity = serializer.validated_data['quantity']
                    witchInventoryIngredient.unit = serializer.validated_data['unit']
                    # Update the added_on field to the current date and time
                    witchInventoryIngredient.added_on = datetime.now()

                    # save new updated object
                    witchInventoryIngredient.save()

                    # serialize again to serialize the new updated object 
                    serializer = MyInventoryIngredientSerializer(witchInventoryIngredient, context={'request': request})
                    return Response(None, status=status.HTTP_204_NO_CONTENT)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else: 
                return Response({'message': 'this ingredient is not a part of your inventory'}, status=status.HTTP_403_FORBIDDEN)
        
        except WitchInventoryIngredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
             # grab the object with pk from client request URL
            witchInventoryIngredient = WitchInventoryIngredient.objects.get(pk=pk)

            # check that the current user trying to delete IS owner of ingredient
            if witchInventoryIngredient.inventory_id == request.auth.user.id:
            
                witchInventoryIngredient.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'this ingredient is not a part of your inventory'}, status=status.HTTP_403_FORBIDDEN)

        except WitchInventoryIngredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)