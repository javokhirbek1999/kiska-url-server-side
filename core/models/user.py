import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


# User models
class UserManager(BaseUserManager):

    """User manager model"""
    def create_user(self, email, user_name, password=None, **extra_fields):
        """Creates and save a new user"""

        if not email:
            raise ValueError(_('Email is required, please enter your email'))
        
        user = self.model(email=self.normalize_email(email), user_name=user_name, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, user_name, password):
        """Creates and saves a new admin user"""
        user = self.create_user(email=email, user_name=user_name, password=password)

        user.is_active = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    email = models.EmailField(max_length=200, unique=True)
    user_name = models.CharField(max_length=200, unique=True, null=True, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['user_name']

    MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    def get_date_joined(self):
        return {
            'day': self.date_joined.day,
            'month': self.MONTHS[self.date_joined.month-1],
            'year': self.date_joined.year
        }
    
    def get_date_updated(self): 
        return {
            'second': self.date_updated.second,
            'minute': self.date_updated.minute,
            'hour': self.date_updated.hour,
            'day': self.date_updated.day,
            'month': self.MONTHS[self.date_updated.month-1],
            'year': self.date_updated.year
        }