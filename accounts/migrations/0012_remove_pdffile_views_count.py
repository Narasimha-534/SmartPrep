# Generated by Django 5.0.6 on 2024-06-22 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_pdffile_views_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdffile',
            name='views_count',
        ),
    ]
