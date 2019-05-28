# Generated by Django 2.2.1 on 2019-05-22 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('code', models.CharField(max_length=10)),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'states',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('status', models.IntegerField()),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.State')),
            ],
            options={
                'db_table': 'cities',
            },
        ),
        migrations.AddField(
            model_name='property',
            name='city',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='property.City'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='state',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='property.State'),
            preserve_default=False,
        ),
    ]
