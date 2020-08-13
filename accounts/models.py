from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, user_id, name, email, password=None):
        if not email:
            raise ValueError('email을 입력해주세요.')

        user = self.model(
            user_id = user_id,
            name = name,
            email = self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_id, name, email, password):
        user = self.create_user(
            user_id,
            name,
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Users(models.Model):
    user_id = models.CharField(max_length=128,unique=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name, email']

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = "users"
