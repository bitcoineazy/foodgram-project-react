from rest_framework import viewsets
from django_filters import rest_framework
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated


from .models import *
from .serializers import *
from .filters import *


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny, )


class RecipesViewSet(viewsets.ModelViewSet):
    filter_backends = [rest_framework.DjangoFilterBackend]
    filter_class = RecipeFilter

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart"
        )

        user_cart = Purchase.objects.filter(user=self.request.user.id)
        is_in_favourites = self.request.query_params.get("is_in_favourites")
        user_favourites = Favourites.objects.filter(user=self.request.user.id)

        if is_in_shopping_cart == "true":
            queryset = queryset.filter(purchase__in=user_cart)
        elif is_in_shopping_cart == "false":
            queryset = queryset.exclude(purchase__in=user_cart)
        if is_in_favourites == "true":
            queryset = queryset.filter(favorites__in=user_favourites)
        elif is_in_favourites == "false":
            queryset = queryset.exclude(favorites__in=user_favourites)
        return queryset.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return RecipeReadSerializer
        return RecipeSerializer

