from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters import rest_framework
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from django.http.response import HttpResponse

from users.serializers import RecipeInSubscriptionSerializer
from .permissions import AdminOrAuthorOrReadOnly
from .models import *
from .serializers import (TagSerializer, IngredientSerializer,
                          FavouriteSerializer, RecipeSerializer,
                          RecipeGetSerializer, OrderSerializer)

from .filters import RecipeFilter, IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None
    filterset_class = IngredientFilter


class RecipesViewSet(viewsets.ModelViewSet):
    filter_backends = [rest_framework.DjangoFilterBackend]
    filter_class = RecipeFilter
    pagination_class = PageNumberPagination
    permission_classes = [AdminOrAuthorOrReadOnly, ]

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        user_cart = Order.objects.filter(user=self.request.user.id)
        is_in_favourites = self.request.query_params.get('is_favorited')
        user_favourites = Favourites.objects.filter(user=self.request.user.id)
        if is_in_shopping_cart == 'true':
            queryset = queryset.filter(order__in=user_cart)
        if is_in_shopping_cart == 'false':
            queryset = queryset.exclude(order__in=user_cart)
        if is_in_favourites == 'true':
            queryset = queryset.filter(favourites__in=user_favourites)
        if is_in_favourites == 'false':
            queryset = queryset.exclude(favourites__in=user_favourites)
        return queryset.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return RecipeGetSerializer
        return RecipeSerializer

    @action(methods=['GET', 'DELETE'],
            url_path='favorite', url_name='favorite',
            permission_classes=[IsAuthenticated], detail=True)
    def favourite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = FavouriteSerializer(
            data={'user': request.user.id, 'recipe': recipe.id})
        if request.method == 'GET':
            serializer.is_valid(raise_exception=True)
            serializer.save(recipe=recipe, user=request.user)
            serializer = RecipeInSubscriptionSerializer(recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)
        favourite = get_object_or_404(
            Favourites, user=request.user, recipe__id=pk)
        favourite.delete()
        return Response(
            data={'message': f'{favourite.recipe} удален из избранного у '
                             f'пользователя {request.user}'},
            status=HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_cart(request):
    user = request.user
    ingredients_in_recipe = IngredientForRecipe.objects.filter(
        recipe__order__user=user
    )
    buying_list = {}
    for item in ingredients_in_recipe:
        amount = item.amount
        name = item.ingredient.name
        measurement_unit = item.ingredient.measurement_unit
        if name not in buying_list:
            buying_list[name] = {
                'amount': amount,
                'measurement_unit': measurement_unit
            }
        else:
            buying_list[name]['amount'] = (
                buying_list[name]['amount'] + amount
            )
    shopping_list = []
    for item in buying_list:
        shopping_list.append(
            f'{item} - {buying_list[item]["amount"]}, '
            f'{buying_list[item]["measurement_unit"]}\n'
        )
    response = HttpResponse(shopping_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = (
        'attachment;' 'filename="shopping_list.txt"'
    )
    return response


class CartView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'delete']

    def get(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = OrderSerializer(
            data={'user': user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(recipe=recipe, user=request.user)
        serializer = RecipeInSubscriptionSerializer(recipe)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        cart = get_object_or_404(Order, user=user, recipe__id=recipe_id)
        cart.delete()
        return Response(
            data={'message': f'Рецепт {cart.recipe} удален из корзины у '
                             f'пользователя {user}'},
            status=HTTP_204_NO_CONTENT)
