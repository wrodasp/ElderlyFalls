# Generated by Django 3.1.7 on 2021-04-14 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.paciente', unique=True),
        ),
    ]