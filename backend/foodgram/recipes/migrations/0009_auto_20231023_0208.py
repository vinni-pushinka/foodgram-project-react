# Generated by Django 3.2 on 2023-10-22 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_recipetag'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_fav',
        ),
        migrations.RemoveConstraint(
            model_name='shoppingcart',
            name='unique_cart',
        ),
    ]