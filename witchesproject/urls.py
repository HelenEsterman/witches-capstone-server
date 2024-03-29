from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from witchesapi.views import WitchUserViewSet, IngredientViewSet, AvatarViewSet, MyInventoryIngredientViewSet, SpellViewSet, UnitViewSet, IngredientTypeViewSet, MyInventoryEquipmentViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'spells', SpellViewSet, 'spell')
router.register(r'ingredients', IngredientViewSet, 'ingredient')
router.register(r'avatars', AvatarViewSet, 'avatar')
router.register(r'myIngredients', MyInventoryIngredientViewSet, 'myIngredient' )
router.register(r'units', UnitViewSet, 'unit' )
router.register(r'types', IngredientTypeViewSet, 'type' )
router.register(r'myEquipment', MyInventoryEquipmentViewSet, 'myEquipment' )

urlpatterns = [
    path('', include(router.urls)),
    path('login', WitchUserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', WitchUserViewSet.as_view({'post': 'register_account'}), name='register'),
 ]

