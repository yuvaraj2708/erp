# Generated by Django 5.0.1 on 2024-02-12 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpapp', '0003_remove_attendance_abscent_attendance_absent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Businessdevelopment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Starting_Date', models.CharField(max_length=255)),
                ('Finishing_Date', models.CharField(max_length=255)),
                ('No_of_Days', models.CharField(max_length=255)),
                ('LPO', models.CharField(max_length=255)),
                ('Invoice_No', models.CharField(max_length=255)),
                ('Amount', models.CharField(max_length=255)),
                ('Total_Amount', models.CharField(max_length=255)),
                ('payable_Pending', models.CharField(max_length=255)),
                ('Comments', models.CharField(max_length=255)),
                ('paid', models.CharField(max_length=255)),
                ('Building_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erpapp.building')),
                ('client_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erpapp.client')),
            ],
        ),
    ]
