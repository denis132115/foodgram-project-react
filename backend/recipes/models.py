from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    """ Модель для тегов рецептов. """
    name = models.CharField(
        max_length=50,
        unique=True, blank=False,
        null=False, verbose_name='Название')
    color = models.CharField(
        max_length=7, blank=False,
        null=False,
        verbose_name='Цвет')
    slug = models.SlugField(
        unique=True, blank=False,
        null=False,
        verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


class Ingredient(models.Model):
    """ Модель для ингредиентов рецептов. """
    name = models.CharField(
        max_length=100, blank=False,
        null=False,
        verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=20, blank=False,
        null=False,
        verbose_name='Единицы измерения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)


class Recipe(models.Model):
    """ Модель для рецептов блюд. """
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
        verbose_name='Картинка')
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
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Количество')

    def __str__(self):
        return (
            f' {self.amount} {self.ingredient}'
            f' для {self.recipe}'
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
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
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
        verbose_name='Рецепт'
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
