# Generated by Django 3.2 on 2023-10-15 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RecipeTag',
        ),
    ]