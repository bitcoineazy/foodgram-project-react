from django.db import models
from django.contrib.auth import get_user_model

from colorfield.fields import ColorField
from django.core.validators import RegexValidator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Имя тега',
        help_text='Введите название тега',
        max_length=200,
        unique=True)
    color = ColorField(
        verbose_name='HEX-код',
        help_text='Введите цветовой HEX-код',
        unique=True,
        null=True)
    slug = models.SlugField(verbose_name='slug', max_length=64, unique=True,
                            validators=[
                                RegexValidator(
                                    regex=r'^[-a-zA-Z0-9_]+$',
                                    message='Недопустимые символы')])

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента')
    measure_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Выберите единицу измерения', )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measure_unit}'


class Recipe(models.Model):
    author_id = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор рецепта')
    name = models.CharField(max_length=50, verbose_name='Название рецепта')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')
    image = models.ImageField(verbose_name='Изображение')
    text = models.TextField(max_length=1000, verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientForRecipe',
        verbose_name='Ингредиенты',
        help_text='Укажите ингредиенты и их количество')
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги', help_text='Выберите один или более тегов')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления, минут', default=1)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='Кол-во', default=1)

    class Meta:
        verbose_name = 'Кол-во ингредиента в рецепте'
        verbose_name_plural = 'Кол-во ингредиента в рецепте'

    def __str__(self):
        return f'{self.recipe}: {self.ingredient}'


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-pub_date']
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_shopping_cart')]

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user}'


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = verbose_name
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_favourite')]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'
