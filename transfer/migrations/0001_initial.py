# Generated by Django 4.2.4 on 2023-08-16 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transfer.user')),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, default=0, max_digits=18)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Failed'), (2, 'Success')], default=0)),
                ('tracker_id', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('destination_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_transactions', to='transfer.wallet')),
                ('source_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_transactions', to='transfer.wallet')),
            ],
        ),
    ]