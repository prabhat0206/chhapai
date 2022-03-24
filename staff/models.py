from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, name, email, ph_number, username, password=None):
        if username is None:
            raise TypeError('User name is required')
        if name is None:
            raise TypeError('Users should have a Name')
        if ph_number is None:
            raise TypeError('Users should have a phone number')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(name=name, email=self.normalize_email(
            email), ph_number=ph_number, username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, ph_number, username, password):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(name, email, ph_number, username)
        user.set_password(password)
        user.superuser = True
        user.staff = True

        user.save()
        return user

    def create_staff(self, name, email, ph_number, username, password):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(name, email, ph_number, username)
        user.set_password(password)
        user.superuser = False
        user.staff = True

        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    ph_number = PhoneNumberField(unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['ph_number', 'name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = Token.for_user(self)
        return{
            'token': str(refresh)
        }
    
    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff
