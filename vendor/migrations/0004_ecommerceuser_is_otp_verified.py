# Generated by Django 4.2.2 on 2023-07-04 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_vendordetail_verify_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecommerceuser',
            name='is_OTP_verified',
            field=models.BooleanField(default=False),
        ),
    ]