from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .models import (
    UserCreditCard, 
    CreditCardType, 
    Categories,
    Rewards,
    Network,
    Issuer,
    UserSettings
    )
from .serializers import (
    UserSerializer, 
    UserCreditCardSerializer, 
    CategorySerializer, 
    CreditCardTypeSerializer,
    UserSettingSerializer,
    )
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status

import datetime
import json
from django.utils.timezone import utc
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import pytz

class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class UserCrediCardViewSet(ModelViewSet):
    serializer_class = UserCreditCardSerializer
    permission_classes=[permissions.IsAuthenticated, ]

    def get_queryset(self):
        return UserCreditCard.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CreditCardTypeViewSet(ReadOnlyModelViewSet):
    queryset = CreditCardType.objects.all()
    serializer_class = CreditCardTypeSerializer
    permission_classes=[permissions.IsAuthenticated, ]

class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes=[permissions.IsAuthenticated, ]


class ComputeBestUserCard(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        credit_cards = UserCreditCard.objects.filter(owner=self.request.user)
        if len(credit_cards) == 0: 
            content = {'Error': 'This User has no credit cards'}
            return  Response(content, status=status.HTTP_412_PRECONDITION_FAILED)

        max_card = credit_cards[0] 
        max_percent_back = 0 
        for cc in credit_cards:
            reward = cc.card_type.rewards_set.filter(category=request.data['category'])
            if reward.exists():
                reward = cc.card_type.rewards_set.get(category=request.data['category'])
                if reward.percent_back > max_percent_back:
                    max_percent_back = max(max_percent_back, reward.percent_back)
                    max_card = cc

        serializer = UserCreditCardSerializer(max_card)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetUserSettings(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try: 
            settings = UserSettings.objects.get(user=self.request.user)
            serialized_data = UserSettingSerializer(settings)
            return Response({"settings":serialized_data.data}, status=status.HTTP_200_OK) 
        except:
            content = {'Error': 'Something went wrong!'}
            return Response(content, status=status.HTTP_412_PRECONDITION_FAILED)


class FlipUserStorageSetting(APIView):
    """
    If a user wants to switch from server to local we return all credit cards! 
        => and wipe our memory clear of them! 
    If a user wants to switch from local to server we parse through credit card objects they create and create them!
        => on local side we should clear their uuid 
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):

        try:
            if self.request.data['store_local'] == 'true':
                print("Setting store local to true")

                #update settings 
                user_setting = UserSettings.objects.get(user=self.request.user)
                user_setting.store_local = True 
                user_setting.save()

                #retrieve all credit cards 
                credit_cards = UserCreditCard.objects.filter(owner=self.request.user)
                serializer = UserCreditCardSerializer(credit_cards, many=True)
                ret_val = Response(serializer.data, status=status.HTTP_200_OK)
                #remove credit cards from server 
                UserCreditCard.objects.filter(owner=self.request.user).delete() 
                return ret_val
            else: 
                print("Setting store local to false")
                #want to store local as credit cards! 
                credit_card_data = request.data['user_credit_cards']
                json_data = json.loads(credit_card_data)

                #popualate table 
                for cc in json_data:
                    cc_type = CreditCardType.objects.get(id=cc["card_type"])
                    new_cc = UserCreditCard(owner=self.request.user,card_type=cc_type, card_number=cc["card_number"], security_code=cc["security_code"], expiration=cc["expiration"])
                    new_cc.save()
                
                #update settings 
                user_setting = UserSettings.objects.get(user=self.request.user)
                user_setting.store_local = False 
                user_setting.save()
        
                return Response({"Sucess":True}, status=status.HTTP_200_OK) 

        except Exception as e:
            print("error",e)
            content = {'Error': 'Something went wrong!'}
            return Response(content, status=status.HTTP_412_PRECONDITION_FAILED)


class InitDatabase(APIView):
    permission_classes = [permissions.IsAdminUser] #need to be an admin user 

    def get(self, request, format=None):
        #creating a category 
        cat = Categories(name='Travel')
        cat.save() 

        #creating a newtork 
        net = Network(name="Visa")
        net.save()

        #creating an Issuer 
        iss = Issuer(name="BOA")
        iss.save()

        #creating a credit card type
        cc_type = CreditCardType(name="Cash Rewards",network=net,issuer=iss)
        cc_type.save() 

        #creating a reward
        r_1 = Rewards(card=cc_type, category=cat,percent_back=3.2)
        r_1.save()

        return  Response({"Success"}, status=status.HTTP_200_OK)

class ObtainExpiringAuthToken(ObtainAuthToken):
    """
    source: https://stackoverflow.com/questions/14567586/token-authentication-for-restful-api-should-the-token-be-periodically-changed
    """

    def post(self, request):
        # from django.utils import timezone
        # now = timezone.now()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.validated_data['user'])
            utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)   
            
            if not created and token.created < utc_now - datetime.timedelta(hours=1):
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = datetime.datetime.utcnow()
                token.save()

            response_data = {'token': token.key}
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)