from django.contrib import admin
from .models import UserCreditCard, CreditCardType, Network, Issuer, Categories, RewardCurrency, SignUpBonus, Reward
# Register your models here.
admin.site.register(UserCreditCard)

class CreditCardTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class RewardAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

#readonly_fields = ('id',)

admin.site.register(CreditCardType, CreditCardTypeAdmin)
admin.site.register(Network)
admin.site.register(Issuer)
admin.site.register(Categories)
admin.site.register(Reward, RewardAdmin)

admin.site.register(SignUpBonus)
admin.site.register(RewardCurrency)