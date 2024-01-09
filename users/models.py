import random
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from users.utils import generate_account_number


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, full_name,  password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, full_name,  password, **other_fields)

    def create_user(self, email, full_name,  password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name,
                          **other_fields)
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    uuid_field = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    full_name = models.CharField(max_length=150, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        # we have overriden the default save method that comes with django itself
        # Generate and assign account number when saving the user

        super().save(*args, **kwargs)


class Account(models.Model):
    uuid_field = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid_field = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    account_number = models.CharField(
        unique=True, max_length=12, null=True, blank=True)
    is_client = models.BooleanField(default=False)
    government_id = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10)
    phone = models.IntegerField(default=000000000)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    # New method to generate account number

    def generate_account_number(self):
        # Logic to generate a unique account number
        # You can customize this based on your requirements
        return generate_account_number(200)

    def save(self, *args, **kwargs):
        # we have overriden the default save method that comes with django itself
        self.name = self.user.full_name
        self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Staff(models.Model):
    uuid_field = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=50)
    is_staff = models.BooleanField(default=False)
    department = models.CharField(_("department"), max_length=50)
    shift = models.CharField(_("shift"), max_length=50)

    def save(self, *args, **kwargs):
        # we have overriden the default save method that comes with django itself
        self.name = self.user.full_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class APIUser(models.Model):
    uuid_field = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=50)
    bank_name = models.CharField(max_length=255)
    api_user = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        # we have overriden the default save method that comes with django itself
        self.name = self.user.full_name
        self.email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
