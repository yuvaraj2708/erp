# Generated by Django 5.0.1 on 2024-02-13 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpapp', '0006_alter_project_workloader_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='projectype',
            field=models.IntegerField(choices=[('AMC', 'AMC'), ('LPO', 'LPO'), ('Workloader', 'Workloader')]),
        ),
    ]