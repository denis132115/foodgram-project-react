from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.db import models


class CustomUser(AbstractUser):
    """ Пользовательская модель. """
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        unique=True,
        error_messages={
            'unique': 'Адрес почты уже используется.'},
        blank=False,
        null=False,
    )
    username = models.CharField(
        max_length=30,
        verbose_name='Имя пользователя',
        unique=True,
        blank=False,
        null=False,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'invalid': (
                'Имя пользователя может содержать только буквы, '
                ' цифры и символы.'
            )
        },
        help_text='Придумайте уникальное имя пользователя.',
    )
    first_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        verbose_name='Фамилия',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'auth_user'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}'


class AuthorSubscription(models.Model):
    """ Модель подписок. """
    subscriber = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author'
    )

    class Meta:
        unique_together = ('author', 'subscriber')
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'
