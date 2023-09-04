from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator


MAX_CHAR_EMAIL = 254
MAX_CHAR_NAME = 30
ERROR_MSG_EMAIL = 'Адрес почты уже используется.'
WARNING_MSG_EMAIL = 'Введите правильный адрес электронной почты.'
HELP_TEXT_USERNAME = 'Придумайте уникальное имя пользователя.'
ERROR_MSG_USERNAME = (
    'Имя пользователя может содержать только буквы, цифры и символы.'
)


class CustomUser(AbstractUser):
    """ Пользовательская модель. """
    email = models.EmailField(
        max_length=MAX_CHAR_EMAIL,
        validators=[EmailValidator(
            WARNING_MSG_EMAIL)],
        verbose_name='Адрес электронной почты',
        unique=True,
        error_messages={
            'unique': ERROR_MSG_EMAIL},
        blank=False,
        null=False,
    )
    username = models.CharField(
        max_length=MAX_CHAR_NAME,
        verbose_name='Имя пользователя',
        unique=True,
        blank=False,
        null=False,
        validators=[UnicodeUsernameValidator()],
        error_messages={'invalid': ERROR_MSG_USERNAME},
        help_text=HELP_TEXT_USERNAME,
    )
    first_name = models.CharField(
        max_length=MAX_CHAR_NAME,
        blank=False,
        null=False,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=MAX_CHAR_NAME,
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

    def get_full_name(self):
        """Можно получить полное имя пользователя:"""
        return f'{self.first_name} {self.last_name}'

    def is_guest(self):
        return not self.is_authenticated

    def is_registered_user(self):
        return self.is_authenticated and not self.is_superuser

    def is_admin(self):
        return self.is_superuser


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
