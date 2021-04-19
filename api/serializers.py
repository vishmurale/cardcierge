from rest_framework import serializers
from .models import UserCreditCard, Categories, CreditCardType, UserSettings, SignUpBonus
from django.contrib.auth.models import User
from django.core.management.utils import get_random_secret_key

class UserSerializer(serializers.ModelSerializer):
    """
    Django User Class Serializer inspired from here: 
    https://stackoverflow.com/questions/16857450/how-to-register-users-in-django-rest-framework
    """
    class Meta:
        model = User
        # fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        fields = ('id', 'username', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            # email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        #default settings 
        key = get_random_secret_key()[0:20]
        obj = UserSettings(key=key, user=user, store_local=False)
        obj.save() 

        return user

class UserCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCreditCard
        fields = ['id', 'owner', 'card_number', 'expiration','security_code', 'card_type', 'welcome_offer', 'open_date', 'reward_value_override']
        write_only_fields = ('card_number',)
        read_only_fields = ('id','owner') 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name',)

class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ('key','user','store_local')

class CreditCardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardType
        fields = ('id', 'name', 'network', 'issuer', 'reward_currency')
        read_only_fields = ('id',)

class SignUpBonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUpBonus
        fields = ('id','spend_amount', 'bonus_amount', 'duration_days', 'card_type')
        read_only_fields = ('id',)