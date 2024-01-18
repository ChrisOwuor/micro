from django.urls import path
from .views import Client_detail, Client_transactions, Clients, Loan_detail, Loans,Disbursements
urlpatterns = [
    path('clients/', Clients.as_view(), name='clients-list'),
    path('client/<int:id>/', Client_detail.as_view(), name='client-detail'),
    path('loans/', Loans.as_view(), name='loan-list'),
    path('loan/<int:id>/', Loan_detail.as_view(), name='loan-detail'),
    path('transaction/', Client_transactions.as_view(), name='client transaction'),
    path('disburse/<int:id>/', Disbursements.as_view(), name='staff disbursement'),

]
