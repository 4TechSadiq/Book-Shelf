from django.db import models
from bookapp.models import book
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomClassManager

# Create your models here.

# class UserTable(models.Model):
#     username = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)
#     rpassword = models.CharField(max_length=200)
    

#     def __str__(self) -> str:
#         return "{}".format(self.username)
    
# class LoginTable(models.Model):
#     username = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)
#     rpassword = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     userType = models.CharField(max_length=200)

#     def __str__(self) -> str:
#         return "{}".format(self.username)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomClassManager()

    def __str__(self):
        return self.email


class Cart(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    items = models.ManyToManyField(book)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    Book = models.ForeignKey(book,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


