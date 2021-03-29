# Generated by Django 3.1.6 on 2021-03-29 19:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCardType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Issuer',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RewardCurrency',
            fields=[
                ('currency_name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('value_percent', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='SignUpBonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spend_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('bonus_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('duration_days', models.DecimalField(decimal_places=2, max_digits=9)),
                ('card_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.creditcardtype')),
            ],
        ),
        migrations.CreateModel(
            name='UserCreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('expiration', models.CharField(max_length=5)),
                ('security_code', models.CharField(max_length=5)),
                ('open_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('reward_value_override', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('card_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.creditcardtype')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('welcome_offer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.signupbonus')),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earn_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.creditcardtype')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.categories')),
            ],
        ),
        migrations.AddField(
            model_name='creditcardtype',
            name='categories',
            field=models.ManyToManyField(through='api.Reward', to='api.Categories'),
        ),
        migrations.AddField(
            model_name='creditcardtype',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.issuer'),
        ),
        migrations.AddField(
            model_name='creditcardtype',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.network'),
        ),
        migrations.AddField(
            model_name='creditcardtype',
            name='reward_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.rewardcurrency'),
        ),
    ]
