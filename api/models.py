from django.db import models
from django.contrib.auth.models import User

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

#available reward categories e.g. Travel 
class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key = True)

    def __str__(self):
        return self.name

#Available Credit Cards Types
class CreditCardType(models.Model):
    name = models.CharField(max_length=20) #e.g "Cash Rewards" 
    network =  models.ForeignKey(Network, on_delete=models.CASCADE) 
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Categories, through='Rewards')

    def __str__(self):
        return str(self.issuer) + ": " + self.name

class Rewards(models.Model):
    card = models.ForeignKey(CreditCardType, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    percent_back = models.DecimalField(max_digits=5, decimal_places=2)

#User Credit Card 
class UserCreditCard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16) #SHOULD NOT STORE THIS PLAINTEXT 
    expiration = models.CharField(max_length=5) #string in format 6/25
    security_code = models.CharField(max_length=5) #SHOULD NOT STORE THIS PLAINTEXT 
    card_type = models.ForeignKey(CreditCardType, on_delete=models.CASCADE)