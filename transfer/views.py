from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from .models import Wallet, Transactions, TrackerId
from .serializers import TransactionSerializer, ScheduleTransactionSerializer, WalletSerializer


def convert_to_schedule(cron_char):
    cron_parts = cron_char.split(' ')
    crontab_schedule = CrontabSchedule.objects.create(
        minute=cron_parts[0],
        hour=cron_parts[1],
        day_of_week=cron_parts[2],
        day_of_month=cron_parts[3],
        month_of_year=cron_parts[4],
    )
    return crontab_schedule


class TransactionCreateView(generics.CreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Transactions.objects.create(serializer.validated_data)
        transaction: Transactions = serializer.save()
        return Response(data={"transaction_status": transaction.get_status_display()}, status=status.HTTP_201_CREATED)


class WalletBalanceView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class ScheduleTransactionCreateView(generics.CreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = ScheduleTransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cron_schedule = convert_to_schedule(serializer.validated_data['crontab_schedule'])
        task = PeriodicTask.objects.create(
            task='transfer.tasks.process_periodic_transaction',
            kwargs=serializer.get_json().decode('utf-8'),
            crontab=cron_schedule,
        )

        return Response({'message': 'Periodic task created successfully.'}, status=status.HTTP_201_CREATED)
