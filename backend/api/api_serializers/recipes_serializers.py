from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import CustomUser, AuthorSubscription
from api.api_serializers.users_serializers import CustomUserSerializer
from recipes.models import (Tag, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart)


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для тегов. """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для ингредиентов. """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeShortSerializer(serializers.ModelSerializer):
    """ Сериализатор для компактного отображения рецептов. """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Subscription ."""

    class Meta:
        model = AuthorSubscription
        fields = ('subscriber', 'author')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для ингредиентов рецепта. """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'id', 'name', 'measurement_unit',)


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели IngredientAmount. """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(required=True, write_only=True,
                                      min_value=1,)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """ Сериализатор списка покупок. """
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')


class SubscriptionShowSerializer(CustomUserSerializer):
    """ Сериализатор отображения подписок. """

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        author_recipes = obj.recipes.all()[:2]
        return RecipeSerializer(
            author_recipes, many=True
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор для рецептов. """
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True,
                                             source='recipeingredient_set')
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_is_favorited(self, obj):
        """ Проверяет, добавлен ли рецепт в избанное. """
        request = self.context.get('request')
        return (
            request is not None
            and not request.user.is_anonymous
            and request.user.favoriting.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """ Проверяет, добавлен ли
        рецепт в список покупок. """
        request = self.context.get('request')
        return (
            request is not None
            and not request.user.is_anonymous
            and request.user.shopping_user.filter(recipe=obj).exists()
        )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time', 'pub_date'
                  )


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True, required=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False)
    tags = serializers.PrimaryKeyRelatedField(many=True, required=True,
                                              queryset=Tag.objects.all())

    @staticmethod
    def create_recipe_ingredients(ingredients_data, recipe_instance):
        """ Добавляет ингредиенты. """
        ingredients_to_create = []
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')

            recipe_ingredient = RecipeIngredient(
                ingredient=ingredient_id,
                recipe=recipe_instance,
                amount=amount
            )

            ingredients_to_create.append(recipe_ingredient)

        RecipeIngredient.objects.bulk_create(ingredients_to_create)

    def create(self, validated_data):
        """ Сохраняет теги и ингредиенты рецепта в базу данных. """
        author = self.context['request'].user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(
            author=author,
            **validated_data
        )

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')
            RecipeIngredient.objects.create(
                ingredient=ingredient_id,
                recipe=recipe,
                amount=amount
            )

        self.create_recipe_ingredients(ingredients_data, recipe)

        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        fields_to_update = ['image', 'name', 'text', 'cooking_time']
        for field_name in fields_to_update:
            new_value = validated_data.get(
                field_name, getattr(instance, field_name))
            setattr(instance, field_name, new_value)

        tags_data = validated_data.get('tags')
        instance.tags.set(tags_data)

        ingredients_data = validated_data.get('ingredients')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.create_recipe_ingredients(ingredients_data, instance)

        instance.save()

        return instance

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'author', 'image', 'name',
                  'text', 'cooking_time', 'pub_date')
