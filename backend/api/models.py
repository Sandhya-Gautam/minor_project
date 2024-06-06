from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email,name, password=None, password2=None):
        
        if not email:
            raise ValueError("Users must have an email address")
        if(password != password2):
            raise ValueError("Two password didnt match")
        
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    Fullname = models.CharField(max_length=200)
    email=models.EmailField(  verbose_name="Email", max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history=models.JSONField (default="", name=Fullname+"history" )

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]


    def __str__(self):
        return self.email

