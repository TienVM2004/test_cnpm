# Generated by Django 4.1.13 on 2024-05-09 12:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0011_alter_folders_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folders',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 9, 12, 33, 9, 333971, tzinfo=datetime.timezone.utc)),
        ),
    ]
