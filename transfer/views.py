import json

from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from .models import Wallet, Transactions
from .serializers import TransactionSerializer, ScheduleTransactionSerializer


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
        tracker_id = serializer.validated_data['tracker_id']
        # Check if tracker_id already exists in Transactions
        if Transactions.objects.filter(tracker_id=tracker_id).exists():
            return Response(
                {"error": "Duplicate tracker ID. This transaction already exists."},
                status=status.HTTP_409_CONFLICT
            )
        transaction: Transactions = serializer.save()
        return Response(data={"transaction_status": transaction.get_status_display()}, status=status.HTTP_201_CREATED)


class WalletBalanceView(APIView):
    def get(self, request, wallet_id):
        wallet = get_object_or_404(Wallet, id=wallet_id)
        return Response({"wallet_id": wallet.id, "balance": wallet.balance}, status=status.HTTP_200_OK)


class ScheduleTransactionCreateView(generics.CreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = ScheduleTransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tracker_id = serializer.validated_data['tracker_id']
        # Check if tracker_id already exists in Transactions
        if Transactions.objects.filter(tracker_id=tracker_id).exists():
            return Response(
                {"error": "Duplicate tracker ID. This transaction already exists."},
                status=status.HTTP_409_CONFLICT
            )
        cron_schedule = convert_to_schedule(serializer.validated_data['crontab_schedule'])
        task = PeriodicTask.objects.create(
            task='transfer.tasks.process_periodic_transaction',
            kwargs=serializer.get_json().decode('utf-8'),
            crontab=cron_schedule,
        )

        return Response({'message': 'Periodic task created successfully.'}, status=status.HTTP_201_CREATED)
