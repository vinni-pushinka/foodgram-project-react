from django.contrib import admin

from users.models import CustomUser, Follow


class UserAdmin(admin.ModelAdmin):
    """Класс для отображения пользователей в админке."""
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Класс для отображения подписок в админке."""
    list_display = ('id', 'user', 'author')


admin.site.register(CustomUser, UserAdmin)
