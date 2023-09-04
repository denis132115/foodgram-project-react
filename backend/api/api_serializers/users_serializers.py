from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from users.models import CustomUser


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
            'is_subscribed'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_subscribed(self, object):
        """ Проверяет, подписан ли текущий пользователь на аккаунт автора. """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return object.author.filter(subscriber=request.user).exists()


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

    def validate(self, data):
        """ Запрещает пользователям присваивать себе username me
        и использовать повторные username и email. """
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        if CustomUser.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Имя пользователя уже существует'
            )
        if CustomUser.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Email уже существует'
            )
        return data
