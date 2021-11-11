from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from recipes.models import Order
from .models import Follow, CustomUser
from .serializers import FollowSerializer, GetFollowingsSerializer


class CustomUserViewSet(UserViewSet):
    @action(detail=True,
            methods=['GET', 'DELETE'],
            url_path='subscribe',
            url_name='subscribe',
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        author = get_object_or_404(CustomUser, id=id)
        serializer = FollowSerializer(
            data={'user': request.user.id, 'author': id})
        if request.method == 'GET':
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            serializer = GetFollowingsSerializer(author)
            return Response(serializer.data, status=HTTP_201_CREATED)
        follow = get_object_or_404(Follow, user=request.user, author__id=id)
        follow.delete()
        return Response(
            {'message': f'{request.user} отписался от {follow.author}'},
                        status=HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['GET'],
            url_path='subscriptions',
            url_name='subscriptions',
            permission_classes=[IsAuthenticated])
    def show_follows(self, request):
        user_obj = CustomUser.objects.filter(
            following__user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        result_page = paginator.paginate_queryset(user_obj, request)
        serializer = GetFollowingsSerializer(
            result_page, many=True, context={'current_user': request.user})
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False,
            methods=['GET'],
            url_path='cart',
            url_name='cart',
            permission_classes=[IsAuthenticated])
    def user_cart(self, request):
        if not Order.objects.filter(user=request.user).exists():
            raise ValidationError(
                {'empty_cart': {'Корзина пуста, перейдите на вкладку'
                                ' рецепты, чтобы обновить список покупок'}})
