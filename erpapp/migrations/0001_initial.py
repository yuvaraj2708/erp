# Generated by Django 5.0.1 on 2024-02-19 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientname', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=50)),
                ('building', models.CharField(max_length=50)),
                ('projectype', models.CharField(choices=[('AMC', 'AMC'), ('LPO', 'LPO'), ('Workorder', 'Workorder')], max_length=20)),
                ('cradle_number', models.CharField(max_length=50)),
                ('starting_date', models.DateField(blank=True, null=True)),
                ('finishing_date', models.DateField(blank=True, null=True)),
                ('number_of_days', models.IntegerField()),
                ('team', models.CharField(max_length=255)),
                ('SubcontratorName', models.CharField(max_length=255)),
                ('Buildingtype', models.CharField(max_length=255)),
                ('No_of_Floors', models.CharField(max_length=255, null=True)),
                ('materials_used', models.TextField()),
                ('receipt', models.CharField(max_length=50)),
                ('invoice_number', models.CharField(max_length=50)),
                ('vat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_received', models.CharField(max_length=255)),
                ('received_date', models.CharField(max_length=255)),
                ('bank_name', models.CharField(max_length=255)),
                ('receivable_pending', models.CharField(max_length=255)),
                ('comments', models.TextField()),
                ('Payable_Pending', models.CharField(max_length=255)),
                ('Subcontrator_invoice', models.CharField(max_length=255)),
                ('cradle_number_input', models.CharField(max_length=255)),
                ('amc_start_date', models.DateField(blank=True, null=True)),
                ('amc_end_date', models.DateField(blank=True, null=True)),
                ('yearly_cycle', models.CharField(blank=True, choices=[('Yearly 1', 'Yearly 1'), ('Yearly 2', 'Yearly 2'), ('Yearly 3', 'Yearly 3'), ('Yearly 4', 'Yearly 4')], max_length=50, null=True)),
                ('lpo_field', models.CharField(blank=True, max_length=50, null=True)),
                ('workorder_type', models.CharField(blank=True, choices=[('Normal 2', 'Normal 2'), ('Normal 3', 'Normal 3'), ('Critical', 'Critical')], max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(max_length=255)),
            ],
        ),
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
        migrations.AddField(
            model_name='building',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='erpapp.client'),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('building_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('Leave_Salary', models.CharField(max_length=255)),
                ('Bonus', models.CharField(max_length=255)),
                ('Overtime', models.CharField(max_length=255)),
                ('Ticket', models.CharField(max_length=255)),
                ('LOP', models.CharField(max_length=255)),
                ('Damage_Deduct', models.CharField(max_length=255)),
                ('other_Deduct', models.CharField(max_length=255)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erpapp.building')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('present', models.BooleanField(default=False)),
                ('leave', models.BooleanField(default=False)),
                ('reason', models.CharField(max_length=50)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erpapp.employee')),
            ],
        ),
        migrations.AddField(
            model_name='building',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='erpapp.supplier'),
        ),
        migrations.CreateModel(
            name='Supplierproject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Starting_Date', models.CharField(max_length=255)),
                ('Finishing_Date', models.CharField(max_length=255)),
                ('No_of_Days', models.CharField(max_length=255)),
                ('LPO', models.CharField(max_length=255)),
                ('Invoice_No', models.CharField(max_length=255)),
                ('VAT', models.CharField(max_length=255)),
                ('Amount', models.CharField(max_length=255)),
                ('Total_Amount', models.CharField(max_length=255)),
                ('payable_Pending', models.CharField(max_length=255)),
                ('Comments', models.CharField(max_length=255)),
                ('paid', models.CharField(max_length=255)),
                ('Building_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erpapp.building')),
                ('supplier_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erpapp.supplier')),
            ],
        ),
    ]
