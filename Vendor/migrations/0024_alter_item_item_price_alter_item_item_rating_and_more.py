# Generated by Django 4.0 on 2022-02-05 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0023_remove_review_likes_review_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_price',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Item Price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_rating',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=2, null=True, verbose_name='Item Rating'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=2, null=True, verbose_name='Shop Rating'),
        ),
    ]
