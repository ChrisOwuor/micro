from .models import Transaction
from .models import Client, Staff, APIUser, Account
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # validated data will be
        #  {
        # 'email': 'example@example.com',
        # 'full_name': 'John Doe',
        # 'password': 'securepassword',
        # 'account_number': 12345678,
        # 'government_id': 98765432
        # }
        # when we call the save method  internally it will pass the validated data
        # to this function so we dont need to explicitelt pass it here
        # so we remove the password from the validated data
        password = validated_data.pop('password', None)

        # instantiatiating the  user model class
        # self.Meta.mode refers to the model associated to the serializer
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # we hash the password
            instance.set_password(password)

            # we call the save method from the user model class this save method is used to store to db
        instance.save()
        # we can now return our stored user
        return instance

    def update(self, instance, validated_data):
        # inside the save method first it will look if there is user instance in the db
        # if it fnds an instance then it will invoke this function if not it will call the
        # create function
        # so its like this to update you specify the url the id you want to update for
        # then now inside the save method we will use the id to get the instance
        # after we get the instance then now we can proceed with the work
        # Update fields based on validated_data
        instance.email = validated_data.get('email', instance.email)
        instance.full_name = validated_data.get(
            'full_name', instance.full_name)

        # Update password if provided
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        # Save the updated instance
        instance.save()
        return instance


# serializers.py


class TransactionSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        required=False, max_digits=10, decimal_places=2)
    transaction_cost = serializers.DecimalField(
        required=False, max_digits=10, decimal_places=2)

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'transaction_date', 'amount',
                  'balance', 'transaction_type', 'transaction_cost')

    def create(self, validated_data):
        transaction_instance = self.Meta.model.objects.create(**validated_data)
        transaction_instance.save()
        return transaction_instance


class ClientSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)

    class Meta:
        model = Client
        fields = ['uuid_field', 'id', 'government_id',
                  'name', 'location', 'age', 'sex', 'phone']

    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        # Set is_client to True by default during creation
        validated_data['is_client'] = True
        # Create a new Client instance linked to the user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.government_id = validated_data.get(
            'government_id', instance.government_id)
        instance.location = validated_data.get('location', instance.location)
        instance.age = validated_data.get('age', instance.age)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.phone = validated_data.get('phone', instance.phone)

        # Save the changes
        instance.save()

        return instance


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['uuid_field', 'holder', 'amount',
                  'account_number', 'account_type', 'created_at']

    def create(self, validated_data):
        # Create a new Client instance linked to the user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['department', 'shift']

    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        # Set is_client to True by default during creation
        validated_data['is_staff'] = True

        # Create a new Client instance linked to the user
        staff = Staff.objects.create(**validated_data)

        return staff  # Add other fields as needed

    def update(self, instance, validated_data):
        # Update fields in the existing Staff instance
        instance.shift = validated_data.get('shift', instance.shift)
        instance.department = validated_data.get(
            'department', instance.department)

        # Save the changes
        instance.save()

        return instance


class APIUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIUser
        fields = ['bank_name', 'api_user', 'email']

    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        # Set is_client to True by default during creation
        validated_data['api_user'] = True

        # Create a new api user instance linked to the user
        api_user = APIUser.objects.create(**validated_data)

        return api_user

    def update(self, instance, validated_data):
        # Update fields in the existing APIUser instance
        instance.bank_name = validated_data.get(
            'bank_name', instance.bank_code)
        # Save the changes
        instance.save()

        return instance
