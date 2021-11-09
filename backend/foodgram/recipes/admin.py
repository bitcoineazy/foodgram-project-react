from django.contrib import admin
from import_export.admin import ImportMixin

from .resources import IngredientResource
from .models import *


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = IngredientResource
    search_fields = ('name',)
    list_filter = ('id', 'name', 'measurement_unit',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')


class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientForRecipe, IngredientForRecipeAdmin)
admin.site.register(Favourites, FavouritesAdmin)
