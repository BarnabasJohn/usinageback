# Generated by Django 5.1.2 on 2024-11-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_alter_client_profile_pic_alter_request2_file1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request2',
            name='file1',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='request2',
            name='file2',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='request2',
            name='file3',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
