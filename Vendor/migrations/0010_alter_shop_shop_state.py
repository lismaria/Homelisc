# Generated by Django 4.0 on 2022-01-22 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0009_alter_shop_shop_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='shop_state',
            field=models.CharField(max_length=50, verbose_name='Shop State'),
        ),
    ]
