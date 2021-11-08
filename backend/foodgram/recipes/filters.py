import django_filters as filters

from .models import Recipe, Ingredient


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name')

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
