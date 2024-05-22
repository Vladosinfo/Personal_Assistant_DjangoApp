# Generated by Django 5.0.6 on 2024-05-21 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_day', models.CharField(max_length=50, unique=True)),
                ('min_temperature', models.CharField(max_length=50, unique=True)),
                ('max_temperature', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='weather',
            constraint=models.UniqueConstraint(fields=('cur_day', 'min_temperature', 'max_temperature'), name='weather'),
        ),
    ]
