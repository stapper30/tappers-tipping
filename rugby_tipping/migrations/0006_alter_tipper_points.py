# Generated by Django 3.2.7 on 2022-10-19 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rugby_tipping', '0005_tipper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipper',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
