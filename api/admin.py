from django.contrib import admin
from .models import Loan, LoanDisbursement, Repayment, APIKey


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ( 'client', 'amount', 'status',
                    'disbursement_date', 'repayment_date', 'loan_type')
    search_fields = ('loan_id', 'client__name')
    list_filter = ('status', 'disbursement_date',
                   'repayment_date', 'loan_type')
    date_hierarchy = 'disbursement_date'


@admin.register(LoanDisbursement)
class LoanDisbursementAdmin(admin.ModelAdmin):
    list_display = ('disbursement_id', 'loan',
                    'disbursed_by', 'disbursement_date')
    search_fields = ('disbursement_id', 'loan__client__name',
                     'disbursed_by__name')
    list_filter = ('disbursement_date',)
    date_hierarchy = 'disbursement_date'


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('repayment_id', 'repayment_for',
                    'amount_paid', 'payment_date', 'remaining_balance')
    search_fields = ('repayment_id', 'repayment_for__loan_id',
                     'repayment_for__client__name')
    list_filter = ('payment_date',)
    date_hierarchy = 'payment_date'


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('api_key_id', 'api_user', 'key', 'valid_until')
    search_fields = ('api_key_id', 'api_user__name')
    list_filter = ('valid_until',)
    date_hierarchy = 'valid_until'
