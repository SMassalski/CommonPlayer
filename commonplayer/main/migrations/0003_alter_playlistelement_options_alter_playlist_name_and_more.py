# Generated by Django 4.0.5 on 2022-06-30 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_medialink_playlist_playlistelement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playlistelement',
            options={'ordering': ('playlist', 'position')},
        ),
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='playlistelement',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='main.playlist'),
        ),
        migrations.AlterUniqueTogether(
            name='playlistelement',
            unique_together={('playlist', 'position')},
        ),
    ]
