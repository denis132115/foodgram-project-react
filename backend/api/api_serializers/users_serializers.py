from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from users.models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    """ Сериализатор для создания объекта класса User. """

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}


class CustomUserSerializer(UserSerializer):
    """ Сериализатор для пользовательской информации.
        Добавляет информацию о подписке пользователя.
    """

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )

    def get_is_subscribed(self, object):
        """ Проверяет, подписан ли текущий пользователь на аккаунт автора. """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return object.author.filter(subscriber=request.user).exists()
