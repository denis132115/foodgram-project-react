from django.contrib import admin

from .models import CustomUser, AuthorSubscription


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """ Админка  для модели пользователя. """
    list_display = (
        'username', 'email', 'first_name',
        'last_name', 'id'
    )
    list_filter = ('username', 'email')
    ordering = ('username',)


@admin.register(AuthorSubscription)
class AuthorSubscriptionAdmin(admin.ModelAdmin):
    """ Админка для подписок на авторов. """
    list_display = ('subscriber', 'author')
