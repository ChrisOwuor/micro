# Generated by Django 5.0 on 2023-12-23 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_phone_alter_user_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
