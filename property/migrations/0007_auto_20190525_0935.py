# Generated by Django 2.2.1 on 2019-05-25 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_auto_20190522_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='max_people',
            field=models.IntegerField(),
        ),
    ]
