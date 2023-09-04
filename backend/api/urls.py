from django.urls import path, include
from rest_framework import routers

from api.api_views import users_views, recipes_views

router = routers.DefaultRouter()
router.register('tags', recipes_views.TagViewSet, basename='tags')
router.register('users', users_views.CustomUserViewSet, basename='users')
router.register('recipes', recipes_views.RecipeViewSet, basename='recipes')
router.register('ingredients', recipes_views.IngredientViewSet,
                basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
