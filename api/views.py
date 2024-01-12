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
import logging
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from users.serializers import ClientSerializer, APIUserSerializer, StaffSerializer, TransactionSerializer
from .serializers import LoanSerializer, LoanDisbursementSerializer, RepaymentSerializer, APIKeySerializer
from users.models import Client, Account
from .models import Loan, LoanDisbursement, Repayment, APIKey
from rest_framework.views import APIView
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated


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
        disbursement_serializer = LoanDisbursementSerializer(data=request.data)
        if disbursement_serializer.is_valid():
            disbursement_serializer.save()
            return Response({'message': 'loan disbused successfully'}, status=status.HTTP_201_CREATED)
        return Response(disbursement_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # get all disbursements

    def get(self, request):
        ...


class Client_transactions(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        client = Client.objects.get(user=request.user)
        if not client:
            return Response({"message": "you are not allowed since you not a client"})
        account = Account.objects.get(holder=99)
        if not account:
            return {"msg": "no account found"}
        transaction_serializer = TransactionSerializer(data=request.data)
        if transaction_serializer.is_valid():
            trans = transaction_serializer.data
            return Response(trans, status=status.HTTP_201_CREATED)
        return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
