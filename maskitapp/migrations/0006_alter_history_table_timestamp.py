# Generated by Django 3.2.1 on 2021-05-09 06:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('maskitapp', '0005_auto_20210508_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history_table',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
