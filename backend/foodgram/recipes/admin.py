from django.contrib import admin
from import_export.admin import ImportMixin

from .models import *


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measure_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author_id')
    list_filter = ('name', 'author_id', 'tags')
    search_fields = ('name', 'author_id', 'tags')


class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientForRecipe, IngredientForRecipeAdmin)
admin.site.register(Favourites, FavouritesAdmin)
