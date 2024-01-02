# Generated by Django 5.0 on 2024-01-02 22:44

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0007_remove_user_account_number_remove_user_government_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('key', models.CharField(max_length=40, unique=True)),
                ('valid_until', models.DateTimeField()),
                ('api_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.apiuser')),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Paid', 'Paid')], max_length=20)),
                ('disbursement_date', models.DateTimeField(blank=True, null=True)),
                ('repayment_date', models.DateTimeField(blank=True, null=True)),
                ('loan_type', models.CharField(blank=True, max_length=50, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.client')),
            ],
        ),
        migrations.CreateModel(
            name='LoanDisbursement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disbursement_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('disbursement_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('disbursed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.staff')),
                ('loan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Repayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repayment_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('remaining_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('repayment_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.loan')),
            ],
        ),
    ]
