# Generated by Django 4.0 on 2022-02-12 18:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0024_alter_item_item_price_alter_item_item_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='shop_tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, verbose_name='Shop Tags'), size=3),
        ),
    ]
