# Generated by Django 3.1.2 on 2020-10-24 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_shipping_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
