# Generated by Django 3.1.7 on 2021-04-06 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20210405_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='tipo',
            field=models.TextField(default='regular', max_length=10),
        ),
    ]