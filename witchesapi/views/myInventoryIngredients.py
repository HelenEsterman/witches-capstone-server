from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from witchesapi.models import WitchInventoryIngredient, WitchInventory, Witch, Ingredient, Unit
from .avatars import AvatarSerializer
from .ingredients import IngredientSerializer
from datetime import datetime

# TODO:also need to finish what I was working on with the 'my' equipment inventory feature

#TODO possible way to solve ingredient measurement and quantity comparison issue!--also refer to sydney's messages for guidance
# utils.py

# Conversion rates from various units to cups
# conversion_rates = {
# 'cup': 1, # 1 cup is the base unit
# 'oz': 0.125, # Assuming 1 cup is 8 oz, so 1 oz is 1/8th of a cup
# 'tbsp': 0.0625, # Assuming 1 cup is 16 tablespoons, so 1 tbsp is 1/16th of a cup
# # Add more conversions as needed
# }

# def convert_to_cups(quantity, unit):
# if unit in conversion_rates:
# return quantity * conversion_rates[unit]
# else:
# # Handle unsupported units
# raise ValueError(f"Unsupported unit: {unit}")


# class IngredientSerializer(serializers.ModelSerializer):
# quantity_in_cups = serializers.SerializerMethodField()

# class Meta:
# model = Ingredient
# fields = ['id', 'name', 'quantity', 'unit', 'quantity_in_cups']

# def get_quantity_in_cups(self, obj):
# # Convert the ingredient quantity to cups
# return convert_to_cups(obj.quantity, obj.unit)
# TODO

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

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'label']

# define a serializer for the inventory ingredients
class MyInventoryIngredientSerializer(serializers.ModelSerializer):
    # serialize inventory obj
    inventory = InventorySerializer(many=False)
    # serialize ingredient obj by importing IngredientSerializer
    ingredient = IngredientSerializer(many=False)

    unit = UnitSerializer(many=False)
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
        #  # get data values from request body
        quantity = request.data['quantity']
        unit_id = request.data['unit']
        ingredient_id = request.data['ingredient']
        inventory_id = request.auth.user.id

        # Check if an inventory ingredient with the same inventory_id, unit_id, and ingredient_id already exists
        existing_ingredient = WitchInventoryIngredient.objects.filter(
            inventory_id=inventory_id,
            unit_id=unit_id,
            ingredient_id=ingredient_id
        ).first()

        if existing_ingredient:
            # If it exists, update the quantity
            existing_ingredient.quantity = quantity
            existing_ingredient.save()
             # Serialize data into json format to be processed
            serializer = MyInventoryIngredientSerializer(existing_ingredient, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # instantiate a witchInventoryIngredient object to have a row PK to work with
            witchInventoryIngredient = WitchInventoryIngredient.objects.create(
                quantity = quantity,
                unit = Unit.objects.get(pk=request.data["unit"]),
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

                    # Check if an inventory ingredient with the same inventory_id, unit_id, and ingredient_id already exists
                    existing_ingredient = WitchInventoryIngredient.objects.filter(
                        inventory_id=request.auth.user.id,
                        unit_id=request.data['unit'],
                        ingredient_id=request.data['ingredient']
                    ).first()
                    if existing_ingredient:
                        # If it exists, update the quantity
                        existing_ingredient.quantity = request.data['quantity']
                        existing_ingredient.save()
                        # Serialize data into json format to be processed
                        serializer = MyInventoryIngredientSerializer(existing_ingredient, context={'request': request})
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                

                
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