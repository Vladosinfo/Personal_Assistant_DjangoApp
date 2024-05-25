# Generated by Django 5.0.6 on 2024-05-25 05:21

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_remove_contact_additional'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='additional_info',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='additional_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]