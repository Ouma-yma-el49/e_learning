# Generated by Django 4.2.16 on 2024-11-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0011_progression'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='progression',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='progression',
            name='chapitre',
        ),
        migrations.RemoveField(
            model_name='progression',
            name='cours',
        ),
        migrations.RemoveField(
            model_name='progression',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='progression',
            name='utilisateur',
        ),
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='cours',
        ),
        migrations.RenameField(
            model_name='chapitre',
            old_name='title',
            new_name='titre',
        ),
        migrations.AddField(
            model_name='chapitre',
            name='fichier',
            field=models.FileField(blank=True, null=True, upload_to='chapitres/'),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Progression',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
    ]
