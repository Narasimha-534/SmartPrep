# Generated by Django 5.0.6 on 2024-06-21 16:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_pdfview'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfview',
            name='uploaded_by',
            field=models.ForeignKey(null=True,blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
