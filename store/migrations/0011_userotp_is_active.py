# Generated by Django 4.2.2 on 2023-07-05 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_userotp_created_date_userotp_is_forgot_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userotp',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]