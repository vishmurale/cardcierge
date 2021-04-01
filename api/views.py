from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .models import (
    UserCreditCard, 
    CreditCardType, 
    Categories,
    Network,
    Issuer,
    RewardCurrency,
    SignUpBonus,
    Reward
    )
from .serializers import (
    UserSerializer, 
    UserCreditCardSerializer, 
    CategorySerializer, 
    CreditCardTypeSerializer,
    SignUpBonusSerializer,
    )
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .categories import categories
import csv
import os
import datetime

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

class SignUpBonusViewSet(ReadOnlyModelViewSet):
    queryset = SignUpBonus.objects.all()
    serializer_class = SignUpBonusSerializer
    permission_classes=[permissions.IsAuthenticated, ]

class ComputeBestUserCard(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        
        LOCAL_STORAGE = True
        if LOCAL_STORAGE: # data stored locally
            # assume we have an list of credit card type ids
            cctype_id_list = [1, 2, 3] # currently hard coded, we should NOT do this

            best_card = cctype_id_list[0] 
            best_payout = 0 

            # we calculate payout with the following:
            #   payout = earn rate * currency value 
            for cctype_id in cctype_id_list:
                cctype = CreditCardType.objects.get(id=cctype_id)

                earn_rate = 0
                multiplier = cctype.reward_currency.value_percent
                
                reward = cctype.reward_set.filter(category=request.data['category'])
                if reward.exists():
                    earn_rate = cctype.reward_set.get(category=request.data['category']).earn_rate
                
                payout = earn_rate * multiplier
                print(f"The payout for {cctype.name} is {payout} and the multiplier is {multiplier} and earn is {earn_rate}")
                if payout > best_payout:
                    best_payout = payout
                    best_card = cctype
            
            serializer = CreditCardTypeSerializer(best_card)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else: # data stored in db on server
            credit_cards = UserCreditCard.objects.filter(owner=self.request.user)
            if len(credit_cards) == 0: 
                content = {'Error': 'This User has no credit cards'}
                return  Response(content, status=status.HTTP_412_PRECONDITION_FAILED)

            best_card = credit_cards[0] 
            best_payout = 0 

            # we calculate payout with the following:
            #   if no SUB attached to card, payout = earn rate * currency value (can be overriden)
            #   if SUB, payout = average payoff of credit card rate
            for cc in credit_cards:
                earn_rate = 0
                multiplier = 0

                if cc.reward_value_override:
                    multiplier = cc.reward_value_override
                else:
                    multiplier = cc.card_type.reward_currency.value_percent

                # check to see if there is SUB
                sub = cc.welcome_offer
                # make sure sub is not expired - if it is expired maybe we shoudl remove it??
                if sub and cc.open_date + datetime.timedelta(days=int(sub.duration_days)) >= datetime.date.today():
                    earn_rate = sub.bonus_amount / sub.spend_amount 
                else:
                    # local_dict['cc'] = cc
                    reward = cc.card_type.reward_set.filter(category=request.data['category'])
                    if reward.exists():
                        earn_rate = cc.card_type.reward_set.get(category=request.data['category']).earn_rate
                    #exec(f"earn_rate = cc.card_type.{request.data['category']}", globals(), local_dict)
                    #earn_rate = local_dict['earn_rate']

                payout = earn_rate * multiplier
                # print(f"The payout for {cc} is {payout} and the multiplier is {multiplier} and earn is {earn_rate}")
                if payout > best_payout:
                    best_payout = payout
                    best_card = cc

            serializer = UserCreditCardSerializer(best_card)
            return Response(serializer.data, status=status.HTTP_200_OK)

class InitDatabase(APIView):
    permission_classes = [permissions.IsAdminUser] #need to be an admin user 

    def get(self, request, format=None):
        #creating all categories
        cats = {}
        for category in categories:
            cats[category] = Categories(name=category)
            cats[category].save() 

        issuers = {}
        networks = {}
        currencies = {}
        cards = {}

        # set up currencies
        with open(os.path.dirname(__file__) + '/../RewardCurrency.csv') as currency_data:
            csv_reader = csv.reader(currency_data, delimiter=",")
            for row in csv_reader:
                if len(row) != 2:
                    print("There is an issue with the currency data - please try a different CSV file")
                    return
                currencies[row[0]] = RewardCurrency(currency_name=row[0], value_percent=float(row[1]))
                currencies[row[0]].save()

        # load all credit card types, along with networks, issuers, and currencies
        with open(os.path.dirname(__file__) + '/../CCdata.csv') as cc_data:
            csv_reader = csv.reader(cc_data, delimiter=",")
            first_line = True
            for row in csv_reader:
                if len(row) != 4 + len(categories):
                    print("There is an issue with the credit card data - please try a different CSV file")
                    return
                # ignore first line
                if first_line:
                    first_line = False
                    continue
                else:
                    name = row[0]
                    issuer = row[1]
                    network = row[2]
                    currency = row[3]

                    if issuer not in issuers:
                        issuers[issuer] = Issuer(name=issuer)
                        issuers[issuer].save()
                    if network not in networks:
                        networks[network] = Network(name=network)
                        networks[network].save()

                    cards[name] = CreditCardType(name=name,network=networks[network],issuer=issuers[issuer],reward_currency=currencies[currency])
                    cards[name].save()

                    # add all categories to card
                    col = 4
                    for category in categories:
                        c = Reward(card=cards[name], category=cats[category], earn_rate=float(row[col]))
                        c.save()
                        col += 1

        # set up SUBs
        with open(os.path.dirname(__file__) + '/../Bonus.csv') as cc_data:
            csv_reader = csv.reader(cc_data, delimiter=",")
            for row in csv_reader:
                if len(row) != 4:
                    print("There is an issue with the bonus data - please try a different CSV file")
                    return

                sub = SignUpBonus(spend_amount=float(row[1]), bonus_amount=float(row[2]), duration_days=float(row[3]), card_type=cards[row[0]])
                sub.save()

        # maybe should come back and add some user ccs for testing 

        return  Response({"Success"}, status=status.HTTP_200_OK)