# Generated by Django 4.2.16 on 2024-11-03 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0003_alter_chapitre_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapitre',
            options={},
        ),
        migrations.RemoveField(
            model_name='chapitre',
            name='order',
        ),
    ]