# Generated by Django 3.0.4 on 2020-04-23 16:24

import accounts.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('f_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('l_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='NP', unique=True)),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Email Address')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2020, 4, 23, 10, 39, 11, 506369, tzinfo=utc), verbose_name='Date of Registration')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('l_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='NP', unique=True)),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Email Address')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2020, 4, 23, 10, 39, 11, 506369, tzinfo=utc), verbose_name='Date of Registration')),
                ('tot_due', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('tot_received', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('image', models.ImageField(default='customer-default.png', upload_to='customers', verbose_name='Image(Customer)')),
            ],
            options={
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('l_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='NP', unique=True)),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Email Address')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2020, 4, 23, 10, 39, 11, 506369, tzinfo=utc), verbose_name='Date of Registration')),
                ('tot_due', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('tot_received', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('image', models.ImageField(default='vendor-default.png', upload_to='vendors', verbose_name='Image(Vendor)')),
            ],
            options={
                'verbose_name_plural': 'Vendors',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('user_avatar', models.ImageField(blank=True, default='default.png', upload_to='profile_avatar', verbose_name='Profile Avatar')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Profiles',
            },
        ),
    ]
