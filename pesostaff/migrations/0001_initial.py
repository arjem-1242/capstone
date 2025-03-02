# Generated by Django 5.1 on 2025-02-08 07:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccreditationRequestApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('approved_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('uploaded_document', models.FileField(blank=True, null=True, upload_to='approval_documents/')),
                ('accreditation_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employer.accreditationrequest')),
            ],
        ),
    ]
