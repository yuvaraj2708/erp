# Generated by Django 5.0.1 on 2024-02-13 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erpapp', '0008_alter_project_projectype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='absent',
            new_name='leave',
        ),
    ]