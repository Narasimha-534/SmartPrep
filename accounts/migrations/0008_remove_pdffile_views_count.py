# Generated by Django 5.0.6 on 2024-06-21 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_pdffile_views_count_alter_pdffile_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdffile',
            name='views_count',
        ),
    ]
