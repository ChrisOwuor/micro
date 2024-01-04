from django.urls import path
from .views import Client_detail, Clients, Loan_detail, Loans
urlpatterns = [
    path('clients/', Clients.as_view(), name='clients-list'),
    path('client/<int:id>/', Client_detail.as_view(), name='client-detail'),
    path('loans/', Loans.as_view(), name='loan-list'),
    path('loan/<int:id>/', Loan_detail.as_view(), name='loan-detail'),

]
