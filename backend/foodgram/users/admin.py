from django.contrib import admin

from .models import Follow, CustomUser


class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user', 'creation_date')
    list_filter = ('creation_date',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    list_filter = ('username', 'email')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Follow, FollowAdmin)
