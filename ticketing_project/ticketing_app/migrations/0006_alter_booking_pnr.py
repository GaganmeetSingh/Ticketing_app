# Generated by Django 3.2.18 on 2023-04-28 13:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing_app', '0005_auto_20230428_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='pnr',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
