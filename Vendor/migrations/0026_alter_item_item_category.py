# Generated by Django 4.0 on 2022-02-13 12:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0025_alter_shop_shop_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, verbose_name='Item Category'), size=3),
        ),
    ]
