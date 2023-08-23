from django.urls import path
from .views import WalletBalanceView,TransactionCreateView,ScheduleTransactionCreateView

urlpatterns = [
    path('transaction/', TransactionCreateView.as_view(), name='transaction-view'),
    path('schedule/', ScheduleTransactionCreateView.as_view(), name='schedule-transaction-view'),
    path('wallet/<int:pk>/wallet-balances/', WalletBalanceView.as_view(), name='wallet-balances'),
]
