# Generated by Django 4.2.16 on 2024-11-08 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0022_alter_message_options_remove_message_expediteur_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='expéditeur',
            new_name='expediteur',
        ),
    ]
