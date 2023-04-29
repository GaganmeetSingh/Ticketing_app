# Generated by Django 3.2.18 on 2023-04-28 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing_app', '0006_alter_booking_pnr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='seat_number',
            field=models.IntegerField(null=True),
        ),
    ]
