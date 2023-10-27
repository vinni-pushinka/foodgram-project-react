from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    email = models.EmailField(
        max_length=254,
        unique=True,
        null=False,
        verbose_name="Адрес электронной почты"
    )

    username = models.CharField(
       max_length=150,
       unique=True,
       null=False,
       verbose_name="Уникальный юзернейм",
       validators=[
           RegexValidator(
               regex=r"^[\w.@+-]+",
               message="Допустимые символы: буквы, цифры и @/./+/-",
           )
        ],
    )

    first_name = models.CharField(
        blank=True, max_length=150, verbose_name="Имя"
    )

    last_name = models.CharField(
        blank=True, max_length=150, verbose_name="Фамилия"
    )

    password = models.CharField(
        blank=False, null=False, max_length=150, verbose_name="Пароль"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Подписчик')

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор')

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
        )
