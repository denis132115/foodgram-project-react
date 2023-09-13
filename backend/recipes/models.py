from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import CustomUser

AMOUNT_MIN = 1
AMOUNT_MAX = 32000


class Tag(models.Model):
    """ Модель для тегов рецептов. """
    name = models.CharField(
        max_length=50,
        unique=True, blank=False,
        verbose_name='Имя тега')
    color = models.CharField(
        max_length=7, blank=False,
        verbose_name='Цвет')
    slug = models.SlugField(
        unique=True, blank=False,
        verbose_name='ID')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    """ Модель для ингредиентов. """
    name = models.CharField(
        max_length=100, blank=False,
        verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=20, blank=False,
        verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """ Модель для рецептов. """
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=False,
        related_name='recipes',
        verbose_name='Автор')
    name = models.CharField(
        max_length=200, blank=False,
        verbose_name='Название')
    image = models.ImageField(
        upload_to='recipes/', blank=False,
        verbose_name='Фото')
    text = models.TextField(
        verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, blank=False,
        verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (минуты)',
        validators=[
            MinValueValidator(AMOUNT_MIN,
                              message='Количество не может быть меньше 1'),
            MaxValueValidator(AMOUNT_MAX,
                              message='Количество не может быть больше 32000')
        ])
    pub_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """ Модель связи рецептов и ингредиентов. """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients_list',
                               verbose_name='Рецепт',)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(AMOUNT_MIN,
                              message='Количество не может быть меньше 1'),
            MaxValueValidator(AMOUNT_MAX,
                              message='Количество не может быть больше 32000')
        ])

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


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

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Рецепт для списка покупок'
        verbose_name_plural = 'Рецепты для списка покупок'
        ordering = ('user',)

    def _str_(self):
        return (f'{self.recipe} в списке покупок у {self.user}')


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
        ordering = ('user',)

    def __str__(self):
        return f'{self.user} - {self.recipe}'
