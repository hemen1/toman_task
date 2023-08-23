from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .serializers import ScheduleTransactionSerializer

@shared_task
def process_periodic_transaction(data):
    serializer = ScheduleTransactionSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
