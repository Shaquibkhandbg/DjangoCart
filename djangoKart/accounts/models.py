from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class MyAccountManager(BaseUserManager):
    
    # for normal user
    def create_user(self,first_name,last_name,email,username,password=None):
        #  Create and return a regular user with an email, username, and password. 
        
        if not email:
            raise ValueError('User must have an email address ')

        if not username:
            raise ValueError('User must have a username')
    

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # for superuser
    def create_superuser(self,first_name,last_name,email,username,password):  
        
        #  Create and return a superuser with an email, username, and password.
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            password= password,
            first_name=first_name,
            last_name=last_name,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
        
        
    

class Account(AbstractBaseUser,PermissionsMixin):
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    username      = models.CharField(max_length=100,unique=True)
    email         = models.EmailField(max_length=100, unique=True)
    phone_number  = models.CharField(max_length=100,)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # required
    date_joined   = models.DateTimeField(auto_now_add=True)
    last_login    = models.DateTimeField(auto_now_add=True)
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'  # Makes email the unique identifier
    REQUIRED_FIELDS = ['username','first_name','last_name']  # Fields required when creating a superuser
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        """
        Return True if the user has a specific permission.
        If the user is an admin, they have all permissions.
        """
        return self.is_admin
    
    def has_module_perms(self,add_label):
        """
        Return True if the user has permission to access the models in a specific app.
        If the user is an admin, they have access to all apps.
        """
        return True
    