# Generated by Django 5.0.1 on 2024-02-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpapp', '0007_alter_project_projectype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='projectype',
            field=models.CharField(choices=[('AMC', 'AMC'), ('LPO', 'LPO'), ('Workloader', 'Workloader')], max_length=20),
        ),
    ]