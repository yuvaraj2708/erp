# Generated by Django 5.0.1 on 2024-03-06 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpapp', '0002_attachment_remove_employee_attachment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='attachments',
        ),
        migrations.AddField(
            model_name='employee',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='employee_attachments/'),
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
    ]