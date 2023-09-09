from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class IngredientSearchFilter(filters.FilterSet):
    """ Фильтр поиска по названию ингредиента. """
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(filters.FilterSet):
    """ Фильтр выборки рецептов по определенным полям. """

    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_favorite_and_cart')
    author = filters.AllValuesMultipleFilter(field_name='author__id')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_favorite_and_cart'
    )

    def filter_favorite_and_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            if self.request.GET.get('is_in_shopping_cart'):
                return queryset.filter(shopping_recipe__user=user)
            else:
                return queryset.filter(favoriting__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited')