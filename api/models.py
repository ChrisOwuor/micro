from django.utils import timezone
import uuid
from django.db import models

from users.models import APIUser, Client, Staff

class Loan(models.Model):
    loan_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[(
        'Pending', 'Pending'), ('Approved', 'Approved'), ('Paid', 'Paid')])
    disbursement_date = models.DateTimeField(null=True, blank=True)
    repayment_date = models.DateTimeField(null=True, blank=True)
    loan_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Loan #{self.loan_id} - {self.client.name}"


class LoanDisbursement(models.Model):
    disbursement_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    disbursed_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    disbursement_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Loan Disbursement #{self.disbursement_id} - {self.loan}"


class Repayment(models.Model):
    repayment_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    repayment_for = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Repayment #{self.repayment_id} - {self.loan}"


class APIKey(models.Model):
    api_key_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    api_user = models.ForeignKey(APIUser, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)
    valid_until = models.DateTimeField()

    def __str__(self):
        return f"API Key #{self.api_key_id} - {self.api_user.name}"
