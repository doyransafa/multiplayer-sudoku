# Generated by Django 4.2.7 on 2023-12-02 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku', '0004_remove_board_solved_board_board_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(default='unnamed room', max_length=100),
            preserve_default=False,
        ),
    ]
