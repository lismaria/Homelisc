from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# what will happen when a new user is created and new super user is created 
# BaseUserManager works bts when new user is created

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):        # Creates and saves a User with the given email and password.
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        # if not is_vendor:
        #     raise ValueError('Users must have a designation')

        user = self.model(
            email = self.normalize_email(email),  # method of BaseUserManager used to lowercase emailid
            name = name, 
            # is_vendor = is_vendor
        )

        user.set_password(password)
        user.save(using=self._db)       # usually defined as "default" from your database configuration in settings.py. Behind the scene self._db set as None. If user.save(using=None), then it will use default database.
        return user


    def create_superuser(self, email, name, password):
        user = self.create_user(
            email = self.normalize_email(email),  
            name = name, 
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=32)
    email = models.EmailField(verbose_name="email", max_length=60 ,unique=True)
    is_vendor = models.BooleanField(default=False)
    profile_pic = models.ImageField(verbose_name="profile pic", default="default.png",blank=True)

    # mandatory fields to create custom user model
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now_add=True)
    is_admin = models.BooleanField(default=False) # a superuser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_superuser = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'        # the field u want the user to login width
    REQUIRED_FIELDS = ['name',]

    # tell the user object where the custom account manager is
    objects = MyUserManager()

    def __str__(self):
        return self.email

    # required for custom user model 

    def has_perm(self, perm, obj=None):     # "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):  # "Does the user have permissions to view the app `app_label`?"
        return True

