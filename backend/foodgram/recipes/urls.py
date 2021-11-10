from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet, RecipesViewSet, CartView
from .utils import download_cart

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('recipes/<int:recipe_id>/shopping_cart/', CartView.as_view()),
    path('recipes/download_shopping_cart/', download_cart,
         name='download_shopping_cart'),
    path('', include(router.urls)),
]
