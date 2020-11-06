# Generated by Django 3.1.2 on 2020-11-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20201026_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='profile_pic',
        ),
        migrations.RemoveField(
            model_name='product',
            name='thumbnail',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, default='', null=True),
        ),
    ]