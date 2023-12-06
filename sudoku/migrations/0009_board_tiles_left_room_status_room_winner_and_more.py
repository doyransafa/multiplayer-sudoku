# Generated by Django 4.2.7 on 2023-12-04 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sudoku', '0008_remove_room_puzzle_room_puzzle'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='tiles_left',
            field=models.SmallIntegerField(default=81),
        ),
        migrations.AddField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('ongoing', 'Ongoing'), ('finished', 'Finished')], default='ongoing', max_length=10),
        ),
        migrations.AddField(
            model_name='room',
            name='winner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='room',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], max_length=6),
        ),
    ]