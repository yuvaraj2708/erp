# Generated by Django 5.0.1 on 2024-02-12 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpapp', '0004_businessdevelopment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workloader',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='amc_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='amc_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='lpo_field',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='workloader_type',
            field=models.CharField(blank=True, choices=[('Normal 1', 'Normal 1'), ('Normal 2', 'Normal 2'), ('Normal 3', 'Normal 3')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='yearly_cycle',
            field=models.CharField(blank=True, choices=[('Yearly 1', 'Yearly 1'), ('Yearly 2', 'Yearly 2'), ('Yearly 3', 'Yearly 3')], max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='AMC',
        ),
        migrations.DeleteModel(
            name='Workloader',
        ),
    ]
