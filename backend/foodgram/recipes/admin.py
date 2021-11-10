from django.contrib import admin
from import_export.admin import ImportMixin

from .models import (Tag, Ingredient, Recipe,
                     IngredientForRecipe, Favourites, Order)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')


class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'pub_date')
    list_filter = ('id', 'user', 'pub_date')
    search_fields = ('user', 'recipe', 'pub_date')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientForRecipe, IngredientForRecipeAdmin)
admin.site.register(Favourites, FavouritesAdmin)
