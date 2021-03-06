from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    username = models.CharField(
        verbose_name='Имя пользователя', unique=True, max_length=100)
    first_name = models.CharField(verbose_name='Имя', max_length=100)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)
    email = models.EmailField(
        verbose_name='Адрес электронной почты', unique=True, max_length=150)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='followers')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')
    creation_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow')]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
