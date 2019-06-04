# Generated by Django 2.2.1 on 2019-05-31 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'cities',
            },
        ),
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
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('latitude', models.CharField(max_length=50, null=True)),
                ('longitude', models.CharField(max_length=50, null=True)),
                ('address1', models.CharField(max_length=500)),
                ('address2', models.CharField(max_length=500, null=True)),
                ('postal', models.CharField(max_length=10)),
                ('availability_type', models.IntegerField(null=True)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(null=True)),
                ('price', models.IntegerField()),
                ('max_people', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(default=True)),
                ('city', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.City')),
                ('state', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.State')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'properties',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField()),
                ('status', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.Property')),
            ],
            options={
                'db_table': 'property_images',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.State'),
        ),
    ]