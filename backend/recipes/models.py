from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    """ Модель для тегов рецептов. """
    name = models.CharField(
        max_length=50,
        unique=True, blank=False,
        verbose_name='Имя тега')
    color = models.CharField(
        max_length=7, blank=False,
        null=False,
        verbose_name='Цвет')
    slug = models.SlugField(
        unique=True, blank=False,
        null=False,
        verbose_name='ID')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


class Ingredient(models.Model):
    """ Модель для ингредиентов. """
    name = models.CharField(
        max_length=100, blank=False,
        null=False,
        verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=20, blank=False,
        null=False,
        verbose_name='Единицы измерения')

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)


class Recipe(models.Model):
    """ Модель для рецептов. """
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=False,
        related_name='recipes',
        null=False,
        verbose_name='Автор')
    name = models.CharField(
        max_length=200, blank=False,
        null=False,
        verbose_name='Название')
    image = models.ImageField(
        upload_to='recipes/', blank=False,
        null=False,
        verbose_name='Фото')
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, blank=False,
        verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name='Время приготовления (минуты)')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)


class RecipeIngredient(models.Model):
    """ Модель связи рецептов и ингредиентов. """
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, message='Количество не может быть меньше 1'),
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'
        ordering = ('recipe',)


class ShoppingCart(models.Model):
    """  Модель списка покупок. """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
        verbose_name='Рецепт'
    )

    def _str_(self):
        return (f'{self.recipe} в списке покупок у {self.user}')

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Рецепт для списка покупок'
        verbose_name_plural = 'Рецепты для списка покупок'
        ordering = ('user',)


class Favorite(models.Model):
    """
    Модель избранных рецептов пользователей.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favoriting',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favoriting',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user} - {self.recipe}'
