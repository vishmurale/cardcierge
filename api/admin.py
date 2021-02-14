from django.contrib import admin
from .models import UserCreditCard, CreditCardType, Network, Issuer, Categories, Rewards
# Register your models here.
admin.site.register(UserCreditCard)

class CreditCardTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class RewardsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(CreditCardType, CreditCardTypeAdmin)
admin.site.register(Network)
admin.site.register(Issuer)
admin.site.register(Categories)
admin.site.register(Rewards, RewardsAdmin)