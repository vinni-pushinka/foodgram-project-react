from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers import FollowListSerializer, FollowSerializer
from users.models import CustomUser, Follow
from users.serializers import CreateCustomUserSerializer, CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет модели пользователей."""

    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny, )

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCustomUserSerializer
        return CustomUserSerializer

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, pk):
        user = self.request.user
        author = get_object_or_404(CustomUser, id=pk)
        data = {
            'user': user.id,
            'author': author.id,
        }
        if request.method == 'POST':
            serializer = FollowSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(
            Follow,
            user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = Follow.objects.filter(user=user)
        authors = [item.author.id for item in subscriptions]
        queryset = CustomUser.objects.filter(pk__in=authors)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
