# Generated by Django 2.2.1 on 2019-05-22 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190521_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login_type',
            field=models.CharField(choices=[('FACEBOOK', 'FACEBOOK'), ('KAKAO', 'KAKAO')], max_length=20),
        ),
    ]
