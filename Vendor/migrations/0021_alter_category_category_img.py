# Generated by Django 4.0 on 2022-02-03 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0020_alter_category_category_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_img',
            field=models.ImageField(blank=True, default='default.png', upload_to='', verbose_name='Category Image'),
        ),
    ]
