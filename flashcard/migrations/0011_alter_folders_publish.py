# Generated by Django 4.1.13 on 2024-04-25 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0010_alter_folders_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folders',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 25, 9, 14, 45, 455657, tzinfo=datetime.timezone.utc)),
        ),
    ]
