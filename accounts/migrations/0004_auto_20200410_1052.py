# Generated by Django 3.0.4 on 2020-04-10 10:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200410_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 10, 5, 7, 50, 863350, tzinfo=utc), verbose_name='Date of Registration'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.IntegerField(max_length=10, unique=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 10, 5, 7, 50, 863350, tzinfo=utc), verbose_name='Registered Date'),
        ),
    ]