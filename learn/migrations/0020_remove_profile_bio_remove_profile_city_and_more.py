# Generated by Django 4.2.16 on 2024-11-08 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0019_alter_profile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='favorite_animal',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='hobby',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='state',
        ),
    ]