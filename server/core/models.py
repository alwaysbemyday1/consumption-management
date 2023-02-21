from django.db import models
from django.contrib.auth.models import BaseUserManager


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