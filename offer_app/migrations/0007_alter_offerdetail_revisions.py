# Generated by Django 5.1.4 on 2025-05-29 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer_app', '0006_alter_offer_options_alter_offerdetail_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerdetail',
            name='revisions',
            field=models.IntegerField(default=-1),
        ),
    ]
