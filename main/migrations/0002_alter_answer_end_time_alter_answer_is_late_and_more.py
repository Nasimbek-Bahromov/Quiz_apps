# Generated by Django 5.0.6 on 2024-08-30 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_late',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
