# Generated by Django 4.1.13 on 2024-03-31 05:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('publish', models.DateTimeField(default=datetime.datetime(2024, 3, 31, 5, 0, 1, 707375, tzinfo=datetime.timezone.utc))),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudySet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('learning_time', models.IntegerField(default=0)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcard.folders')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ori_word', models.CharField(max_length=30)),
                ('trans_word', models.CharField(max_length=150)),
                ('or_lan', models.CharField(choices=[('en', 'English'), ('vi', 'Vietnamese')], default='en', max_length=3)),
                ('ne_lan', models.CharField(choices=[('en', 'English'), ('vi', 'Vietnamese')], default='vi', max_length=3)),
                ('studyset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcard.studyset')),
            ],
        ),
    ]
