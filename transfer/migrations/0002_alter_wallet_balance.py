# Generated by Django 4.2.4 on 2023-08-19 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=18),
        ),
    ]
