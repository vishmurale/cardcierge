from django.db import models
from django.contrib.auth.models import User
from .categories import categories
from datetime import date

# Create your models here.

#available Network e.g. Visa 
class Network(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key = True)
    
    def __str__(self):
        return self.name

#available Issuer e.g. BOA 
class Issuer(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key = True) 

    def __str__(self):
        return self.name

# #available reward categories e.g. Travel 
class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key = True)

    def __str__(self):
        return self.name

# reward currency
class RewardCurrency(models.Model):
    currency_name = models.CharField(max_length=255, unique=True, primary_key = True)
    value_percent = models.DecimalField(max_digits=4, decimal_places=2)
    
    def __str__(self):
        return self.currency_name


#Available Credit Cards Types
class CreditCardType(models.Model):
    # basic info
    name = models.CharField(max_length=20) #e.g "Cash Rewards" 
    network =  models.ForeignKey(Network, on_delete=models.CASCADE) 
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE)
    reward_currency = models.ForeignKey(RewardCurrency, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Categories, through='Reward')

    # # define all the categories, which are mutually exclusive
    # for category in categories:
    #     exec(f"{category} = models.DecimalField(max_digits=4, decimal_places=2)")
    
    def __str__(self):
        return str(self.issuer) + ": " + self.name

class Reward(models.Model):
    card = models.ForeignKey(CreditCardType, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    earn_rate = models.DecimalField(max_digits=5, decimal_places=2)

# welcome offers 
class SignUpBonus(models.Model):
    spend_amount = models.DecimalField(max_digits=9, decimal_places=2)
    bonus_amount = models.DecimalField(max_digits=9, decimal_places=2)
    duration_days = models.DecimalField(max_digits=9, decimal_places=2)
    
    # each SUB is related to a cc type - may need to tweak this model 
    card_type = models.ForeignKey(CreditCardType, on_delete=models.CASCADE)

    def __str__(self):
        return f"SUB:Spend${self.spend_amount}Get{self.bonus_amount}pts{self.duration_days}days"

#User Credit Card 
class UserCreditCard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16) #SHOULD NOT STORE THIS PLAINTEXT 
    expiration = models.CharField(max_length=5) #string in format 6/25
    security_code = models.CharField(max_length=5) #SHOULD NOT STORE THIS PLAINTEXT 
    card_type = models.ForeignKey(CreditCardType, on_delete=models.CASCADE)

    # these are all optional - maybe open date should be mandatory?
    # need to find a way to limit choices of welcome offer, but it is dependent on card_type, which makes it hard
    # limit_choices_to
    welcome_offer = models.ForeignKey(SignUpBonus, on_delete=models.CASCADE, null=True, blank=True)
    open_date = models.DateField(default=date.today, null=True, blank=True)

    # a user can provide this value to override the default valuation
    # it would be nice to be able to display the default valuation 
    reward_value_override = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.owner} - {self.card_type}"
