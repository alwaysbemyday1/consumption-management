from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
   use_in_migrations = True
   
   def create_user(self, email, password):
       if not email:
           raise ValueError('email does not exist')
       if not password:
           raise ValueError('password does not exist')

       user = self.model(
           email=self.normalize_email(email),
       )
       user.set_password(password)
       user.save(using=self._db)
       return user

   def create_superuser(self, email, password):
       user = self.create_user(email = self.normalize_email(email), password=password)
       user.is_admin = True
       user.is_superuser = True
       user.save(using=self._db)
       return user

class User(AbstractBaseUser, PermissionsMixin):
   objects = UserManager()
   
   email = models.EmailField(max_length=255, unique=True)
   is_active = models.BooleanField(default=True)
   is_admin = models.BooleanField(default=False)

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = []

   def __str__(self):
       return self.email

   @property
   def is_staff(self):
       return self.is_admin

class Ledger(models.Model):
    user = models.ForeignKey(User, db_column="user_id", on_delete=models.CASCADE, related_name='ledger')
    amount = models.IntegerField()
    memo = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)