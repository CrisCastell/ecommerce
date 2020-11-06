# Generated by Django 3.1.2 on 2020-10-23 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='no-image.jpg', null=True, upload_to='products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, default='no-image-thumbnail.jpg', null=True, upload_to='products'),
        ),
    ]
