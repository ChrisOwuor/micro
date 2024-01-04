from rest_framework.authtoken.views import obtain_auth_token
from .views import ClientCreateView, APIUserCreateView, Client, StaffCreateView, ClientUpdateView
from django.urls import path, include
from .views import CustomUserCreate, BlacklistTokenUpdateView, MyTokenObtainPairView, ClientUpdateView


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
    path('auth/update/client/<int:id>/',
         ClientUpdateView.as_view(), name='update-client'),
    # register users
    path('auth/register/', CustomUserCreate.as_view(), name='register-user'),
    # login registered users
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #     create aand update client account
    path('auth/create/client/', ClientCreateView.as_view(), name='create-client'),
    #     create and update api user account
    path('auth/create/apiuser/', APIUserCreateView.as_view(), name='create-apiuser'),
    #     create and update  staff account
    path('auth/create/staff/', StaffCreateView.as_view(), name='create-staff'),
]
