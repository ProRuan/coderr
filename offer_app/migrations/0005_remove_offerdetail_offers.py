# Generated by Django 5.1.4 on 2025-05-26 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer_app', '0004_offerdetail_offers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offerdetail',
            name='offers',
        ),
    ]
