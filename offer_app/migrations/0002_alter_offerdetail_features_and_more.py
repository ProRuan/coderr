# Generated by Django 5.1.4 on 2025-05-23 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerdetail',
            name='features',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='offerdetail',
            name='offer_type',
            field=models.CharField(default='basic', max_length=50),
        ),
    ]
