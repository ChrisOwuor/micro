from rest_framework import serializers
from .models import Loan, LoanDisbursement, Repayment, APIKey
from users.serializers import APIUserSerializer, ClientSerializer, StaffSerializer


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ['loan_id', 'client', 'amount', 'status',
                  'disbursement_date', 'repayment_date', 'loan_type']


class LoanDisbursementSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanDisbursement
        fields = ['disbursement_id', 'loan',
                  'disbursed_by', 'disbursement_date']


class RepaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repayment
        fields = ['repayment_id', 'repayment_for',
                  'amount_paid', 'payment_date', 'remaining_balance']


class APIKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = APIKey
        fields = ['api_key_id', 'api_user', 'key', 'valid_until']
