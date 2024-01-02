from rest_framework.authtoken.views import obtain_auth_token
from .views import ClientCreateView, APIUserCreateView, Clients, StaffCreateView, ClientUpdateView
from django.urls import path, include
from .views import CustomUserCreate, BlacklistTokenUpdateView, MyTokenObtainPairView, ClientUpdateView, Single_client

from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
app_name = 'users'

urlpatterns = [

    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),

    path('auth/view/clients/',
         Clients.as_view(), name='all-clients'),
    path('auth/update/client/<int:id>/',
         ClientUpdateView.as_view(), name='update-client'),
    path('auth/single/client/<int:id>/',
         Single_client.as_view(), name='single-client'),
    path('auth/register/', CustomUserCreate.as_view(), name='register-user'),
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/create/client/', ClientCreateView.as_view(), name='create-client'),
    path('auth/create/apiuser/', APIUserCreateView.as_view(), name='create-apiuser'),
    path('auth/create/staff/', StaffCreateView.as_view(), name='create-staff'),
]
