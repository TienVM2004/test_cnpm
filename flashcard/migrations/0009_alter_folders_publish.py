# Generated by Django 4.1.13 on 2024-04-14 09:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0008_rename_author_studyset_user_alter_folders_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folders',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 14, 9, 36, 1, 107464, tzinfo=datetime.timezone.utc)),
        ),
    ]
