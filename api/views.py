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
    )
from .serializers import (
    UserSerializer, 
    UserCreditCardSerializer, 
    CategorySerializer, 
    CreditCardTypeSerializer,
    )
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status

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

    def get(self, request, format=None):
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