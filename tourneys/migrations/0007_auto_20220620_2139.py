# Generated by Django 3.2.12 on 2022-06-21 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourneys', '0006_auto_20220612_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetrial',
            name='mid_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tournament',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
