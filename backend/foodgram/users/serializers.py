from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Follow, CustomUser
from recipes.models import Recipe


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class RecipeInSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class GetFollowingsSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count']

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return RecipeInSubscriptionSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        return queryset.count()


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    author = serializers.IntegerField(source='author.id')

    class Meta:
        model = Follow
        fields = ['user', 'author']

    def validate(self, data):
        user = data['user']['id']
        author = data['author']['id']
        follow_exist = Follow.objects.filter(
            user=user, author__id=author).exists()
        if user == author:
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на самого себя'})
        elif follow_exist:
            raise serializers.ValidationError({'errors': 'Уже подписаны'})
        return data

    def create(self, validated_data):
        author = validated_data.get('author')
        author = get_object_or_404(CustomUser, pk=author.get('id'))
        user = validated_data.get('user')
        return Follow.objects.create(user=user, author=author)
