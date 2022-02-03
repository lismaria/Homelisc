# Generated by Django 4.0 on 2022-02-03 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0019_remove_category_item_id_remove_category_shop_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_count',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Category Count'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_img',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='', verbose_name='Category Image'),
        ),
    ]
