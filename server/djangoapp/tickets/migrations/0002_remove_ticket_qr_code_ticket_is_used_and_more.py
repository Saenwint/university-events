# Generated by Django 5.2 on 2025-04-17 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='unique_code',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
