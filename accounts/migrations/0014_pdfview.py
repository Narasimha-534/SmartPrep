# Generated by Django 5.0.6 on 2024-06-22 06:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_pdffile_views_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_on', models.DateTimeField(auto_now_add=True)),
                ('pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.pdffile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'pdf')},
            },
        ),
    ]
