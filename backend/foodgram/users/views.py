from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.serializers import (
    UserFollowSerializer,
    CurrentSertializer,
    FollowListSerializer
)
from rest_framework.permissions import IsAuthenticated
from users.models import User, Follow
from rest_framework.decorators import action
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination


class CustomUserViewSet(UserViewSet):
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = CurrentSertializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        data = {
            'following': id,
            'user': user.id
        }
        following = get_object_or_404(User, id=id)
        if user == following:
            return Response(
                {'errors': 'Вы не можете подписаться на самого себя '},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Follow.objects.filter(user=user, following=following).exists():
            return Response(
                {'errors': 'Подписка уже создана'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserFollowSerializer(data=data,
                                          context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def unsubscribe(self, request, id=None):
        user = request.user
        following = get_object_or_404(User, id=id)
        Follow.objects.filter(user=user, following=following).delete()
        Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serilaizer = FollowListSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serilaizer.data)
