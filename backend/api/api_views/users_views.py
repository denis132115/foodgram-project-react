from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from djoser.views import UserViewSet

from users.models import CustomUser, AuthorSubscription
from api.api_serializers.users_serializers import (CustomUserSerializer)
from api.api_serializers.recipes_serializers import (
    SubscriptionSerializer,
    SubscriptionShowSerializer)
from api.pagination import CustomPagination
from api.permissions import AnonimOrAuthenticatedReadOnly


class CustomUserViewSet(UserViewSet):
    """ Пользователи: просмотр и управление. """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    permission_classes = [AnonimOrAuthenticatedReadOnly]

    @action(detail=False, methods=['get', 'post'])
    def me(self, request):
        """ Мои данные: получение и обновление. """
        if not request.user.is_authenticated:
            return Response({'Детали': 'Вы не авторизованны.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_subscribe(self, request, id):
        """ Позволяет пользователю подписываться/отписываться
        от автора контента. """
        author = get_object_or_404(CustomUser, id=id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data={'subscriber': request.user.id, 'author': author.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            author_serializer = SubscriptionShowSerializer(
                author, context={'request': request}
            )
            return Response(
                author_serializer.data, status=status.HTTP_201_CREATED
            )
        subscription = get_object_or_404(
            AuthorSubscription, subscriber=request.user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_subscriptions(self, request):
        """ Возвращает авторов, на которых подписан
         пользователь. """
        authors = CustomUser.objects.filter(author__subscriber=request.user)
        paginator = CustomPagination()
        result_pages = paginator.paginate_queryset(
            queryset=authors, request=request
        )
        serializer = SubscriptionShowSerializer(
            result_pages, context={'request': request}, many=True
        )
        return paginator.get_paginated_response(serializer.data)
