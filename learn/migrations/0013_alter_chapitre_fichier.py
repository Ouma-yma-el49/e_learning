# Generated by Django 4.2.16 on 2024-11-06 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0012_alter_progression_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapitre',
            name='fichier',
            field=models.FileField(upload_to='learn/media/'),
        ),
    ]