# Generated by Django 4.0 on 2022-01-22 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0010_alter_shop_shop_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='shop_clicks_count',
            field=models.IntegerField(default=None, verbose_name='Shop Clicks Count'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_rating',
            field=models.FloatField(default=None, verbose_name='Shop Rating'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_wishlist_count',
            field=models.IntegerField(default=None, verbose_name='Shop Wishlist Count'),
        ),
    ]
