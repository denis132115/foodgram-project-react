from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Favorite)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


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
    list_display = ('user', 'recipe')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ Админка для модели Recipe. """
    list_display = ('name', 'author',
                    'get_favorite_count')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientInline,)

    def get_favorite_count(self, obj):
        """ Получает общее количество избранных рецептов. """
        return obj.favoriting.count()

    get_favorite_count.short_description = 'Избранное'
