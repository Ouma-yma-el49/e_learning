# Generated by Django 4.2.16 on 2024-11-09 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0028_rename_timestamp_message_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
