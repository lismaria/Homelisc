# Generated by Django 4.0 on 2022-01-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0007_shopreview_shop_review_img_shopwishlist_itemwishlist_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='shop_area',
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_state',
            field=models.CharField(default=None, max_length=50, verbose_name='Shop State'),
        ),
    ]
