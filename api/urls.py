from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views


router = routers.DefaultRouter()
router.register(r'creditcards', views.UserCrediCardViewSet, basename='creditcard') 
router.register(r'categories', views.CategoryViewSet, basename='category') 
router.register(r'credit_types', views.CreditCardTypeViewSet, basename='credit_type') 
router.register(r'subs', views.SignUpBonusViewSet, basename='sub') 
# we can register like this and itll import all routes 
# see here for more: https://www.django-rest-framework.org/api-guide/routers/

urlpatterns = [
    path('', include(router.urls)),
    path('account/register', views.CreateUserView.as_view()), 
    path('token/obtain', views.ObtainExpiringAuthToken.as_view(), name='token_obtain'),
    path('getusersettings', views.GetUserSettings.as_view()),
    path('flipuserstorage', views.FlipUserStorageSetting.as_view()),
    path('getbestcard', views.ComputeBestUserCard.as_view()),
    path('infercategory', views.InferCategory.as_view()),
    path('init_database', views.InitDatabase.as_view()), 
]