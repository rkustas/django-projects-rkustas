# Generated by Django 3.1.7 on 2021-03-15 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todolist',
            old_name='dueDate',
            new_name='due_date',
        ),
    ]
