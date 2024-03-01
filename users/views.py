from django.shortcuts import get_object_or_404
from .serializers import ClientSerializer, APIUserSerializer, StaffSerializer, AccountSerializer
from .models import Client, APIUser, Staff, Account
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['full_name'] = user.full_name
        token["email"] = user.email
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Accont creation for all the users of the sytem the staff and the client 
# accounts will be created in this view
class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):

        # intantiating the CustomUserSerializer class and passing raw data to it now this data is what will be validated the data
        # may look like this {
        # 'email': 'example@example.com',
        # 'full_name': 'John Doe',
        # 'password': 'securepassword',
        # 'account_number': 12345678,
        # 'government_id': 98765432
        # }
        serializer = CustomUserSerializer(data=request.data)

        # in our serializer class we have some validations as shown below
        # email = serializers.EmailField(required=True)
        # full_name = serializers.CharField(required=True)
        # password = serializers.CharField(min_length=8, write_only=True)
        # account_number = serializers.IntegerField(unique=True, write_only=True)
        # government_id = serializers.IntegerField(unique=True, write_only=True)
        # for example email must be a valid email and fullname must be a character
        if serializer.is_valid():
            # Check if the email is unique before saving
            # serializer.is_valid() returns a boolean (True or False).
            # serializer.validated_data contains the cleaned and validated data after a successful call to serializer.is_valid()
            email = serializer.validated_data.get('email')
            full_name = serializer.validated_data.get('full_name')
            if not self.is_name_unique(full_name):
                return Response({'name': ['This name is already in use.']}, status=status.HTTP_400_BAD_REQUEST)
            if not self.is_email_unique(email):
                return Response({'email': ['This email address is already in use.']}, status=status.HTTP_400_BAD_REQUEST)
            # so if the above is valid we call the create or update  method in the serilizer class by default
            # so what create function does it creates an instace of the user model then uses the save method to store data into the db
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_email_unique(self, email):
        # Check if the email is unique in your database
        # You can implement your database query logic here
        # For example, assuming your User model is called CustomUser:

        return not User.objects.filter(email=email).exists()

    def is_name_unique(self, full_name):
        # Check if the email is unique in your database
        # You can implement your database query logic here
        # For example, assuming your User model is called CustomUser:

        return not User.objects.filter(full_name=full_name).exists()


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# for staff and admin


class ClientUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        user = request.user
        user_dict = {
            "status": user.is_active,
            "staff": user.is_staff,
            "email": user.email,
            "full_name": user.full_name
        }
        print(request.user.id)
        instance = get_object_or_404(Client, id=id)
        serializer = ClientSerializer(
            instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Client updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# After creating the account users will now
# create the client account here by providing the personal details
# after saving the client data we will use the saved client to create an
# account  fo the client
class ClientCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ClientSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            client_instance = serializer.save()

            # Create an Account instance and associate it with the client
            account_instance = Account.objects.create(
                holder=client_instance,
                amount=0.0,
                account_type='Savings'
            )
            account = AccountSerializer(account_instance).data
            return Response({'message': 'Client account created successfully', "account": account, "client": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        instance = get_object_or_404(Client, user=request.user)

        serializer = ClientSerializer(
            data=request.data, context={'user': request.user}, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Client account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUserCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = APIUserSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Api user account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        instance = get_object_or_404(APIUser, user=request.user)
        serializer = APIUserSerializer(
            data=request.data, context={'user': request.user}, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'api user account updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StaffSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Client account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        instance = get_object_or_404(Staff, user=request.user)
        serializer = StaffSerializer(
            data=request.data, context={'user': request.user}, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Client account updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
