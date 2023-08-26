import logging

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from .models import Wallet, Transactions
from django.db.transaction import atomic
from django.db.models import Case, When, Value, BooleanField, F, Q
from cron_validator import CronValidator


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'balance']


class TransactionSerializer(serializers.Serializer):
    source_user_id = serializers.IntegerField()
    destination_user_id = serializers.IntegerField()
    source_wallet_id = serializers.IntegerField()
    destination_wallet_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=0, default=0)
    tracker_id = serializers.CharField()

    def validate(self, data):
        if data['source_wallet_id'] == data['destination_wallet_id']:
            raise serializers.ValidationError("Source wallet and Destination wallet are same.")

        source_wallet = Wallet.objects.filter(user_id=data['source_user_id'], id=data['source_wallet_id']).first()
        destination_wallet = Wallet.objects.filter(user_id=data['destination_user_id'],
                                                   id=data['destination_wallet_id']).first()
        if not source_wallet:
            raise serializers.ValidationError("Source wallet does not exist for the given user.")

        if not destination_wallet:
            raise serializers.ValidationError("Destination wallet does not exist for the given user.")

        if source_wallet.balance < data['amount']:
            raise serializers.ValidationError("Insufficient balance in the source wallet.")

        return data

    def create(self, validated_data):
        logger = logging.getLogger('transaction_logger')
        amount = validated_data['amount']
        tracker_id = validated_data['tracker_id']

        try:
            with atomic():
                # Deduct amount from source wallet
                affected_rows = Wallet.objects.filter(
                    user_id=validated_data['source_user_id'],
                    id=validated_data['source_wallet_id'],
                    balance__gte=amount
                ).update(balance=F('balance') - amount)

                # if there is Insufficient balance affected_rows will be 0
                if affected_rows != 1:
                    raise ValueError("Insufficient balance in the source wallet.")

                # Add amount to destination wallet
                Wallet.objects.filter(
                    user_id=validated_data['destination_user_id'],
                    id=validated_data['destination_wallet_id']).update(balance=F('balance') + amount)

                transaction_status = Transactions.Status.success
            # Log the successful transaction
            logger.info(f"Transaction successful - Tracker ID: {tracker_id}")

        except Exception as e:
            transaction_status = Transactions.Status.failed
            # Log the failed transaction
            logger.error(f"Transaction failed - Tracker ID: {tracker_id}, Error: {str(e)}")

        # Create transaction instance
        transaction = Transactions.objects.filter(tracker_id=tracker_id).update(status=transaction_status)
        return transaction


class ScheduleTransactionSerializer(TransactionSerializer):
    crontab_schedule = serializers.CharField()

    def validate_crontab_schedule(self, value):
        if len(value.split(' ')) != 5:
            raise serializers.ValidationError("Crontab is not valid.")

        try:
            CronValidator.parse(value)
            return value
        except:
            raise serializers.ValidationError("Crontab is not valid.")

    def get_json(self):
        return JSONRenderer().render({'data': self.data})
