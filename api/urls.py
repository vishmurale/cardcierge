from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views


router = routers.DefaultRouter()
# router.register(r'heroes', views.HeroViewSet) we can register like this and itll import all routes 

urlpatterns = [
    path('', include(router.urls)),
    path('account/register', views.CreateUserView.as_view()), 
    path('token/obtain', obtain_auth_token, name='token_obtain'),
]