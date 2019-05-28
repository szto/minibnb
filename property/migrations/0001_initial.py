# Generated by Django 2.2.1 on 2019-05-21 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_auto_20190521_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('availability_type', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.IntegerField()),
                ('max_people', models.CharField(max_length=10)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('status', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'properties',
            },
        ),
    ]
