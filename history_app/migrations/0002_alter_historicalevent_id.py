# Generated by Django 5.1.7 on 2025-03-16 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalevent',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
