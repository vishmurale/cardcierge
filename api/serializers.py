from rest_framework import serializers
from .models import UserCreditCard, Categories, CreditCardType
from django.contrib.auth.models import User

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

        return user

class UserCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCreditCard
        fields = ['id', 'owner', 'card_number', 'expiration','security_code', 'card_type']
        write_only_fields = ('card_number',)
        read_only_fields = ('id','owner') 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name',)

class CreditCardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardType
        fields = ('id', 'name', 'network', 'issuer')
        read_only_fields = ('id',)