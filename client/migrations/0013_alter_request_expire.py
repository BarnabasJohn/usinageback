# Generated by Django 5.1.2 on 2024-11-03 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_remove_request_deadline_request_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='expire',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
