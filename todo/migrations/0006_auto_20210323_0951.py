# Generated by Django 3.1.7 on 2021-03-23 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20210318_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='createdAt',
            field=models.DateField(default='2021-03-23'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(default='2021-03-23'),
        ),
    ]