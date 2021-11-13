from django.shortcuts import get_object_or_404
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from users.serializers import CustomUserSerializer
from .models import (Tag, Ingredient, IngredientForRecipe, Favourites,
                     Recipe, Order)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = IngredientForRecipe
        fields = ['id', 'name', 'amount', 'measurement_unit']


class IngredientForRecipeCreateSerializer(IngredientForRecipeSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    def to_representation(self, instance):
        ingredient_in_recipe = [
            item for item in
            IngredientForRecipe.objects.filter(ingredient=instance)]
        return IngredientForRecipeSerializer(ingredient_in_recipe).data


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientForRecipeCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        ingredients = data['ingredients']
        exist_recipe = Recipe.objects.filter(name=data['name']).exists()
        if request.method == 'POST' and exist_recipe:
            raise serializers.ValidationError({
                'errors': f"Рецепт с таким названием: {data['name']} уже "
                          f"существует"})
        if data['cooking_time'] < 1:
            raise serializers.ValidationError(
                {'cooking_time':
                    'Время приготовления не может быть меньше 1'})
        unique_ingredients = set()
        for ingredient in ingredients:
            if ingredient['id'] in unique_ingredients:
                raise serializers.ValidationError(
                    {'errors': 'Такой ингредиент уже существует'})
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    {'amount': f'Кол-во ингредиента должно быть больше 0'})
            unique_ingredients.add(ingredient['id'])
        return data

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Order.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favourites.objects.filter(
            user=request.user, recipe=obj).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=request.user, **validated_data)
        recipe.tags.set(tags_data)
        ingredient_in_recipe = [IngredientForRecipe(
            recipe=recipe,
            ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
            amount=ingredient['amount']) for ingredient in ingredients]
        IngredientForRecipe.objects.bulk_create(ingredient_in_recipe)
        recipe.save()
        return recipe

    def update(self, recipe, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe_data = Recipe.objects.filter(id=recipe.id)
        recipe_data.update(**validated_data)
        ingredients_instance = [
            ingredient for ingredient in recipe.ingredients.all()]
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            ingredient_id = ingredient['id']
            if IngredientForRecipe.objects.filter(
                    id=ingredient_id, amount=amount).exists():
                ingredients_instance.remove(
                    IngredientForRecipe.objects.get(id=ingredient_id,
                                                    amount=amount).ingredient)
            else:
                IngredientForRecipe.objects.get_or_create(
                    recipe=recipe,
                    ingredient=get_object_or_404(
                        Ingredient, id=ingredient_id), amount=amount)
        if validated_data.get('image') is not None:
            recipe.image = validated_data.get('image', recipe.image)
        recipe.ingredients.remove(*ingredients_instance)
        recipe.tags.set(tags_data)
        return recipe


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
            raise serializers.ValidationError({'errors': 'Уже в избранном'})
        return data

    def create(self, validated_data):
        user = validated_data['user']
        recipe = validated_data['recipe']
        Favourites.objects.get_or_create(user=user, recipe=recipe)
        return validated_data


class RecipeGetSerializer(RecipeSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = IngredientForRecipe.objects.filter(recipe=obj)
        return IngredientForRecipeSerializer(ingredients, many=True).data


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        user = data['user']['id']
        recipe = data['recipe']['id']
        if Order.objects.filter(user=user, recipe__id=recipe).exists():
            raise serializers.ValidationError(
                {'errors': 'Рецепт уже в корзине'})
        return data
