from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination

from users.models import CustomUser, AuthorSubscription
from api.api_serializers.users_serializers import CustomUserSerializer
from api.api_serializers.recipes_serializers import (
    SubscriptionSerializer,
    SubscriptionShowSerializer)
from api.permissions import AnonimOrAuthenticatedReadOnly


class CustomUserViewSet(UserViewSet):
    """ Пользователи: просмотр и управление. """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AnonimOrAuthenticatedReadOnly]

    @action(detail=False, methods=['get', 'patch'],
            url_path='my-profile', url_name='my-profile')
    def profile(self, request):
        if request.method == 'PATCH':
            useer_serializer = CustomUserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            useer_serializer.is_valid(raise_exception=True)
            useer_serializer.save()
            return Response(useer_serializer.data, status=status.HTTP_200_OK)

        serializer = CustomUserSerializer(
            request.user, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'],
            url_path='subscribe', url_name='subscribe',
            permission_classes=(permissions.IsAuthenticated,))
    def manage_subscription(self, request, id):
        """ Позволяет пользователю подписываться/отписываться
        от автора контента. """
        user = request.user
        content_author = get_object_or_404(CustomUser, id=id)

        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data={'subscriber': user.id, 'author': content_author.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_serializer = SubscriptionShowSerializer(
                content_author, context={'request': request}
            )
            return Response(
                user_serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            subscription_object = get_object_or_404(
                AuthorSubscription, subscriber=user, author=content_author
            )
            subscription_object.delete()
            authors = CustomUser.objects.filter(author__subscriber=user)
            paginator = PageNumberPagination()
            obj = paginator.paginate_queryset(
                queryset=authors, request=request)
            serializer = SubscriptionShowSerializer(
                obj, context={'request': request}, many=True
            )
            return paginator.get_paginated_response(serializer.data)

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        """ Возвращает авторов, на которых подписан
        пользователь. """
        user = request.user
        subscriptions = CustomUser.objects.filter(author__subscriber=user)
        paginator = PageNumberPagination()
        obj = paginator.paginate_queryset(
            queryset=subscriptions, request=request)
        serializer = SubscriptionShowSerializer(
            obj, context={'request': request}, many=True
        )
        return paginator.get_paginated_response(serializer.data)
