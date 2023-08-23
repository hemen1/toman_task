import factory
import random
import uuid
from transfer.models import User, Wallet, Transactions
import json


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker('name', )


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    user = factory.LazyAttribute(lambda _: User.objects.order_by('?').first() or UserFactory())
    balance = factory.LazyAttribute(lambda _: random.randint(1000, 100_000_000_000))


class TransactionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transactions

    source_wallet_id = factory.LazyAttribute(lambda _: Wallet.objects.order_by('?').first())
    destination_wallet_id = factory.LazyAttribute(lambda _: Wallet.objects.order_by('?').first())
    amount = factory.LazyAttribute(lambda _: random.randint(1000, 100_000_000_000))
    tracker_id = factory.LazyAttribute(lambda _: uuid.uuid1())


UserFactory.create_batch(10)
WalletFactory.create_batch(20)
transactions = factory.build_batch(dict, FACTORY_CLASS=TransactionsFactory, size=50)
data = []
for transaction in transactions:
    data.append({'source_wallet_id': transaction['source_wallet_id'].id,
                 'destination_wallet_id': transaction['destination_wallet_id'].id,
                 'amount': transaction['amount'],
                 'tracker_id': str(transaction['tracker_id']),
                 'source_user_id': transaction['source_wallet_id'].user.id,
                 'destination_user_id': transaction['destination_wallet_id'].user.id})
with open('transaction_data.json', 'w') as json_file:
    json.dump(data, json_file)
