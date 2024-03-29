# Generated by Django 4.0 on 2022-01-17 08:48

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0002_shop_shop_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50, verbose_name='Item Name')),
                ('item_descr', models.TextField(verbose_name='Item Description')),
                ('item_rating', models.FloatField(verbose_name='Item Rating')),
                ('item_price', models.FloatField(verbose_name='Item Price')),
                ('item_clicks_count', models.IntegerField(verbose_name='Item Clicks Count')),
                ('item_wishlist_count', models.IntegerField(verbose_name='Item Wishlist Count')),
                ('item_category', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, verbose_name='Item Category'), size=None)),
                ('shop_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Vendor.shop')),
            ],
        ),
    ]
