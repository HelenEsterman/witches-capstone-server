from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from witchesapi.views import WitchUserViewSet, SpellViewSet, WitchIngredientViewSet, AvatarViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'spells', SpellViewSet, 'spell')
router.register(r'witchIngredients', WitchIngredientViewSet, 'witchIngredient')
router.register(r'avatars', AvatarViewSet, 'avatar')

urlpatterns = [
    path('', include(router.urls)),
    path('login', WitchUserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', WitchUserViewSet.as_view({'post': 'register_account'}), name='register'),
]

