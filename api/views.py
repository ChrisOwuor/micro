# staff
# view all clients ,single client
# disburse loans
# view loan history
# view payment history
# api user
# view single client details
# view loan history
# view payment history
# reports
# all loans
# client statement
# client
# apply loan
# withdraw loan
# repay loan
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from users.serializers import ClientSerializer, APIUserSerializer, StaffSerializer, TransactionSerializer
from .serializers import LoanSerializer, LoanDisbursementSerializer, RepaymentSerializer, APIKeySerializer
from users.models import Client, Account, Staff, User
from .models import Loan, LoanDisbursement, Repayment, APIKey
from rest_framework.views import APIView
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated

from users.utils import calculate_transaction_cost


class Client_detail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            instance = Client.objects.get(id=id)
            serializer = ClientSerializer(instance).data
            return Response(serializer, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({"detail": "Client not found"}, status=status.HTTP_404_NOT_FOUND)


class Clients(APIView):
    #  view all clients ,single client
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instance = Client.objects.all()
        serializer = ClientSerializer(instance, many=True).data
        if serializer:
            return Response(serializer, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Loan_detail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            loan_instance = Loan.objects.get(id=id)
        except Loan.DoesNotExist:
            # Log the error and return a generic response
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

        loan_data = LoanSerializer(loan_instance).data

        repayment_instance = Repayment.objects.filter(
            repayment_for=loan_instance)
        loan_repayments_data = RepaymentSerializer(
            repayment_instance, many=True).data

        # Include repayments data in the loan_data response
        loan_data["repayments"] = loan_repayments_data

        return Response(loan_data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        loan = get_object_or_404(Loan, id=id)

        # Check if the logged-in user is the owner of the loan
        if request.user.id != loan.client.id:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        loan.delete()
        return Response({'message': 'Loan deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    # Update (edit) a loan
    def put(self, request, id):
        loan = get_object_or_404(Loan, id=id)
        user = request.user
        client = Client.objects.get(user=user)
        # Check if the logged-in user is the owner of the loan
        if loan.client != client:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = LoanSerializer(loan, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Loan updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Loans(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loan_instance = Loan.objects.all()
        serializer = LoanSerializer(loan_instance, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # client to apply loan

    def post(self, request):
        amount = request.data.get('amount')
        loan_type = request.data.get('loan_type')

        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create a new loan details
        loan_data = {
            'client': client.id,
            'amount': amount,
            'status': 'Pending',
            'loan_type': loan_type
        }

        loan_serializer = LoanSerializer(data=loan_data, partial=True)

        if loan_serializer.is_valid():
            loan_serializer.save()
            return Response({'message': 'Loan applied successfully'}, status=status.HTTP_201_CREATED)
        return Response(loan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     # Delete a loan


class Disbursements(APIView):
    permission_classes = [IsAuthenticated]
    # make loan disbursement

    def post(self, request, id):
        loan_to_disbusrse = Loan.objects.get(id=id)
        disbursed_by = Staff.objects.get(user=request.user)
        print(loan_to_disbusrse)
        print(disbursed_by)
        # disbursement_serializer = LoanDisbursementSerializer(data=request.data)
        # if disbursement_serializer.is_valid():
        #     disbursement_serializer.save()
        #     return Response({'message': 'loan disbused successfully'}, status=status.HTTP_201_CREATED)
        return Response({"found"}, status=status.HTTP_200_OK)
    # get all disbursements

    # def post(self, request):
    #     ...


class Client_transactions(APIView):
    permission_classes = [IsAuthenticated]
    # withdrawal and deposit request

    def post(self, request):
        client = Client.objects.get(user=request.user)
        if not client:
            return Response({"msg": "non client cannot perfom transactions"})
        account = Account.objects.get(holder=client)
        if not account:
            return {"msg": "no account found"}

        data = {
            "account": account.id,
            "amount": float(request.data.get("amount", 0.00)),
            "transaction_type": request.data.get("transaction_type",)
        }
        account_balance = account.amount
        transaction_serializer = TransactionSerializer(data=data)
        if transaction_serializer.is_valid():
            transaction = transaction_serializer.data
            transacion_type = transaction.get("transaction_type")
            if transacion_type == "withdraw":
                amount = float(transaction.get("amount", 0.00))
                transaction_cost = float(
                    calculate_transaction_cost(amount, transacion_type))
                total_deduction = amount+transaction_cost
                balance = float(float(account.amount) -
                                (amount+transaction_cost))
                if account_balance < total_deduction:
                    return Response({"insufficient funds "}, status=status.HTTP_201_CREATED)
                transaction["transaction_cost"] = transaction_cost
                transaction["balance"] = balance

                return Response(transaction, status=status.HTTP_201_CREATED)
            elif transacion_type == "deposit":
                amount = float(transaction.get("amount", 0.00))

                transaction_cost = float(
                    calculate_transaction_cost(amount, transacion_type))
                balance = float(float(account.amount) +
                                (amount+transaction_cost))
                transaction["transaction_cost"] = transaction_cost
                transaction["balance"] = balance

                return Response(transaction, status=status.HTTP_201_CREATED)

        return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
