from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField

from .models import *

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_in_favourites = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        return data

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Purchase.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_favourites(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favourites.objects.filter(user=request.user, recipe=obj).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags_data)
        ingredient_in_recipe = [IngredientForRecipe(
            recipe=recipe,
            ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
            amount=ingredient['amount']
        )
            for ingredient in ingredients
        ]
        IngredientForRecipe.objects.bulk_create(ingredient_in_recipe)
        recipe.save()
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe.ingredients.clear()
        ingredient_in_recipe = [IngredientForRecipe(
            recipe=recipe,
            ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
            amount=ingredient['amount']
        )
            for ingredient in ingredients
        ]
        IngredientForRecipe.objects.bulk_create(ingredient_in_recipe)
        if validated_data.get('image') is not None:
            recipe.image = validated_data.get('image', recipe.image)
        recipe.tags.set(tags_data)
        return super().update(recipe, validated_data)


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = IngredientForRecipe
        fields = ['id', 'name', 'amount', 'measurement_unit']


class FavouriteSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = Favourites
        fields = ['user', 'recipe']

    def validate(self, data):
        user = data['user']['id']
        recipe = data['recipe']['id']
        if Favourites.objects.filter(user=user, recipe__id=recipe).exists():
            raise serializers.ValidationError({"errors": "Уже в избранном"})
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        recipe = validated_data["recipe"]
        Favourites.objects.get_or_create(user=user, recipe=recipe)
        return validated_data
