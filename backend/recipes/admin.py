from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Favorite)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Админка для модели Tag. """
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """ Админка для модели Ingredient. """
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ Админка для модели Recipe. """
    list_display = ('name', 'author',
                    'get_total_favorite_count', 'get_ingredients')
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('ingredients', 'tags')

    def get_total_favorite_count(self, obj):
        """ Получает общее количество избранных рецептов. """
        return obj.favoriting.count()

    get_total_favorite_count.short_description = 'Избранное'

    def get_ingredients(self, object):
        """ Получает ингредиент или список ингредиентов рецепта. """
        return '\n'.join(
            (ingredient.name for ingredient in object.ingredients.all())
        )

    get_ingredients.short_description = 'Ингредиенты'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """ Админика для модели RecipeIngredient. """
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(ShoppingCart)
class ShoppingcartAdmin(admin.ModelAdmin):
    """ Админка для модели ShoppingListItem. """
    list_display = ('recipe', 'user')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """ Админка для модели FavoriteRecipe. """
    list_display = ('user', 'recipe', 'added_at')
