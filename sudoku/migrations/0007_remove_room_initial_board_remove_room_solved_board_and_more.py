# Generated by Django 4.2.7 on 2023-12-03 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku', '0006_puzzle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='initial_board',
        ),
        migrations.RemoveField(
            model_name='room',
            name='solved_board',
        ),
        migrations.AddField(
            model_name='room',
            name='puzzle',
            field=models.ManyToManyField(to='sudoku.puzzle'),
        ),
    ]
