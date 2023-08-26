from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserModel(AbstractUser):
    pass


class Wallet(models.Model):
    user = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=18, decimal_places=0)


class Transactions(models.Model):
    class Status(models.IntegerChoices):
        pending = 0
        in_progress = 1
        failed = 2
        success = 3

    source_wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE, related_name='source_transactions')
    destination_wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE, related_name='destination_transactions')
    amount = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    status = models.IntegerField(choices=Status.choices, default=Status.pending)
    tracker_id = models.CharField(max_length=32, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
