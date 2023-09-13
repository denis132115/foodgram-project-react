from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from recipes.models import (
    Tag, Ingredient, Recipe, Favorite, ShoppingCart, RecipeIngredient)
from api.api_views.utils import create_shopping_cart
from api.api_serializers.recipes_serializers import (
    TagSerializer, IngredientSerializer,
    RecipeSerializer, RecipeCreateSerializer,
    RecipeShortSerializer)
from .filters import RecipeFilter, IngredientSearchFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Просмотр тегов. Только чтение. """
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Просмотр ингредиентов. Только чтение. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientSearchFilter
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """ Просмотр и управление рецептами.
      Чтение, создание, обновление, удаление.
    """
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=['post', 'delete'],
            url_path='shopping_cart', url_name='shopping_cart',
            permission_classes=(permissions.IsAuthenticated,))
    def get_shopping_cart(self, request, pk=None):
        """ Добавляет или удаляет рецепт из
          корзины покупок текущего пользователя. """
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            ShoppingCart.objects.get_or_create(user=request.user,
                                               recipe=recipe)
            status_code = status.HTTP_201_CREATED
        else:
            request.user.shopping_user.filter(recipe=recipe).delete()
            status_code = status.HTTP_204_NO_CONTENT

        shopping_cart_serializer = RecipeShortSerializer(recipe)
        return Response(shopping_cart_serializer.data, status=status_code)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart',
            url_name='download_shopping_cart',
            permission_classes=(permissions.IsAuthenticated,)
            )
    def download_shopping_cart(self, request):
        """ Позволяет пользователю загрузить список покупок. """
        user = request.user
        recipe_ingredients_query = (
            RecipeIngredient.objects.filter(
                recipe__shopping_recipe__user=user
            ).values('ingredient__name', 'ingredient__measurement_unit',
                     ).order_by('ingredient__name').annotate(
                         ingredient_amount=Sum('amount')))
        return create_shopping_cart(recipe_ingredients_query)

    @action(detail=True, methods=['post', 'delete'], url_path='favorite',
            url_name='favorite', permission_classes=(
                permissions.IsAuthenticated,))
    def get_favorite(self, request, pk):
        """ Позволяет пользователю добавлять рецепты в избранное. """
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        data = {
            'user': user.pk,
            'recipe': recipe.pk
        }

        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(user=user,
                                                               recipe=recipe)
            if created:
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            favorite_recipe = get_object_or_404(Favorite,
                                                user=user, recipe=recipe)
            favorite_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
